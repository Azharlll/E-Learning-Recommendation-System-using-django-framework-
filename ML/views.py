from django.shortcuts import render, get_object_or_404, redirect
from .models import Users,Notes,UserActivityPath
from django.db.models import Avg, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import connection
from django.utils import timezone
#from .moresecrets import youtube_search
from .forms import UsersForm,NotesForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http import HttpResponseRedirect,JsonResponse
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.views.generic import TemplateView
import json
from mysql.connector import MySQLConnection, Error
import csv
import operator

# Create your views here.
def index(request):

    return render(request, 'e_learning/home.html')



# Login view for the page.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in the user
            user = form.get_user()
            login(request,user)
            return redirect('index')

    else:
        form = AuthenticationForm()
    return render(request,'e_learning/login.html',{'form':form})



#Renders the signout page.
def signout(request):
    if request.POST:
        return search(request, request.POST["search"])
    else:
        logout(request)
        return render(request, 'e_learning/logout.html')

#Renders the Users registration Page.
def register(request):
    if request.method == 'POST':
        user_form_web = UsersForm(request.POST, prefix='rater')
        user_form_admin = UserCreationForm(request.POST, prefix='user')
        if user_form_web.is_valid() * user_form_admin.is_valid():
            user = user_form_admin.save(commit=False)
            user.save()
            weber = user_form_web.save(commit=False)
            weber.users_id = user.id
            #weber.id = user.id
            weber.save()
            return HttpResponseRedirect('/')
    else:
        user_form_web = UsersForm(prefix='rater')
        user_form_admin = UserCreationForm(prefix='user')
    context = {'raterform': user_form_web,'userform': user_form_admin}
    return render(request, 'e_learning/signup.html', context)

#Function to get the user activity from each media page.
def activity(request):
    user = request.user
    pausecount = request.GET.get('pausecount', None)
    seekcount  = request.GET.get('seekcount', None)
    replaycount = request.GET.get('replaycount', None)
    paths = request.GET.get('paths', None)
    data = {
        'is_taken': True
    }
    print(pausecount,seekcount,replaycount)
    usa = UserActivityPath.objects.create(user=user,date=timezone.now(),seeking=seekcount,pauses=pausecount,replaycount=replaycount, path=paths)
    return JsonResponse(data)

#Renders the page displaying the video,audio or ppt as per the requested url.
def media(request):
    offset = request.GET['offset']
    Title,Summary,view_count=query_with_fetchone(offset)

    if request.user.is_authenticated:
        if request.method == 'POST':
                form = NotesForm(request.POST,prefix='notes')

                if form.is_valid():
                    instance = form.save(commit=False)
                    Notes.date = timezone.now()
                    instance.author = request.user
                    instance.types = request.path
                    instance.save()
                return redirect('media')
        else:
            form = NotesForm(prefix='notes')

        return render(request, 'e_learning/media.html',{"form":form,"author_id":request.user,"paths":request.path,"file":offset,"Title":Title,"Summary":Summary,"view_count":view_count})
    else:
        return redirect('login')


from configparser import ConfigParser



#function to fetch video details from extranal database to django.
def query_with_fetchone(vname):
 try:
     #dbconfig = read_db_config()
     conn = MySQLConnection(user='work', password='work1234',host='127.0.0.1',database='demo')
     cursor = conn.cursor()
     cursor.execute("SELECT actual_name, summary,view_count FROM video where video_name = %s",(vname,))
     row = cursor.fetchone()
     hitcount = row[2]+1
     cursor.execute("update video set view_count = %s where video_name = %s",(hitcount,vname,));
     conn.commit()

     while row is not None:
         return row[0],row[1],row[2]
         #row = cursor.fetchone()
 except Error as e:
     print(e)

 finally:
     cursor.close()
     conn.close()

#Function needed for online recommendation which could be developed more in future projects
# Right now the work is carried out offline my ELearning.
def recommendation(request):

    def train():
        import pandas as pd
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn import model_selection
        from sklearn.cross_validation import train_test_split #split the data into train and test data
        import MySQLdb
        mysql_cn= MySQLdb.connect(host='localhost',port=3306,user='work', password='work1234',db='demo9')

        data=pd.read_sql('select * from Postprocessing_tab',con = mysql_cn)
        n1=len(data)
        l=list(data[0:0])
        l1=l.index('Q1M5')

        def model_KNN(qs,qe,st):
            KNN1=pd.DataFrame(data.iloc[0:n1,qs:qe])
            KNN2=pd.DataFrame(data.iloc[0:n1,st])
            X_train, X_test, y_train, y_test = train_test_split(KNN1, KNN2, test_size = 0.25, random_state = 0)
            clf = KNeighborsClassifier(n_neighbors=3)
            clf.fit(X_train,y_train.values.ravel())
            test=clf.predict(X_test)
            kfold = model_selection.KFold(n_splits=15)
            accuracy = model_selection.cross_val_score(clf,X_train,y_train.values.ravel(), cv=kfold)
            return test,accuracy.mean()*100

        vocab=model_KNN(l1,l1+9,l1+63)
        print("Vocabulary Section: ",vocab[0])
        print("accuracy Vocabulary: ",vocab[1])

        grammar=model_KNN(l1+9,l1+18,l1+64)
        print("Grammar Section",grammar[0])
        print("accuracy Vocabulary: ",grammar[1])

        reading=model_KNN(l1+18,l1+30,l1+65)
        print("Reading Section",reading[0])
        print("accuracy Reading: ",reading[1])

        Computer=model_KNN(l1+30,l1+35,l1+66)
        print("Computer Section",Computer[0])
        print("accuracy Computer: ",Computer[1])

        writing=model_KNN(l1+35,l1+38,l1+67)
        print("Writing Section",writing[0])
        print("accuracy Writing: ",writing[1])

        video=model_KNN(l1+38,l1+41,l1+68)
        print("Video Section",video[0])
        print("accuracy video: ",video[1])

        audio=model_KNN(l1+41,l1+44,l1+69)
        print("Audio Section",audio[0])
        print("accuracy audio: ",audio[1])

        PPT=model_KNN(l1+44,l1+47,l1+70)
        print("PPT Section",PPT[0])
        print("accuracy PPT: ",PPT[1])

    #def recommend():

#Processed labels of recommendation and chart data is passed for rendering to display to 
# the individual user.
def test(request):
    if request.user.is_authenticated:
        user = request.user
        t = Users.objects.get(users_id=user.id)
        t_admin = User.objects.get(id=user.id)
        name = t.name
        web_name = t_admin.username

        try:

            conn = MySQLConnection(user='work', password='work1234',host='127.0.0.1',database='demo10')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Postprocessing_tab where Firstname = %s",(web_name,))
            row = cursor.fetchone()

            conn.commit()

            cursor.execute("select Firstname,VocabTotal from Postprocessing_tab order by VocabTotal desc limit 5")
            RowVoc = cursor.fetchall()
            cursor.execute("select Firstname,GrammarTotal from Postprocessing_tab order by GrammarTotal desc limit 5")
            RowGra = cursor.fetchall()
            cursor.execute("select Firstname,ReadingTotal from Postprocessing_tab order by ReadingTotal desc limit 5")
            RowRea = cursor.fetchall()
            cursor.execute("select Firstname,ComputerTotal from Postprocessing_tab order by ComputerTotal desc limit 5")
            RowComp = cursor.fetchall()
            cursor.execute("select Firstname,WritingTotal from Postprocessing_tab order by WritingTotal desc limit 5")
            RowWri = cursor.fetchall()

            cursor.execute("select VocabTotal from Postprocessing_tab order by VocabTotal desc limit 1")
            TopVoc = cursor.fetchone()

            cursor.execute("select GrammarTotal from Postprocessing_tab order by GrammarTotal desc limit 1")
            TopGra = cursor.fetchone()

            cursor.execute("select ReadingTotal from Postprocessing_tab order by ReadingTotal desc limit 1")
            TopRea = cursor.fetchone()

            cursor.execute("select ComputerTotal from Postprocessing_tab order by ComputerTotal desc limit 1")
            TopComp = cursor.fetchone()

            cursor.execute("select WritingTotal from Postprocessing_tab order by WritingTotal desc limit 1")
            TopWri = cursor.fetchone()

            translator = {'Basic':'B','Intermediate':'I','Advanced':'A'}
            VocabLabel = translator[row[-8]]
            GrammarLabel = translator[row[-7]]
            ReadingLabel = translator[row[-6]]
            ComputerLabel = translator[row[-5]]
            WritingLabel = translator[row[-4]]

            Score_translator = {'Most_Interested':3,'Moderatly_Interested':2, 'Not_so_Interested':1}
            m_l = {'VideoLabel':'V','AudioLabel':'A','PPTLabel':'P'}

            Mediallabel = {'VideoLabel':Score_translator[row[-3]],'AudioLabel':Score_translator[row[-2]],'PPTLabel':Score_translator[row[-1]]}
            level = m_l[max(Mediallabel.items(),key=operator.itemgetter(1))[0]]


            cursor.execute("select video_name,actual_name,video_thumbnail from demo.video where moduleType = 'V' and Type = %s and  modetype <> %s",(level,VocabLabel,))
            VocabularyMaterials = cursor.fetchall()

            cursor.execute("select video_name,actual_name,video_thumbnail from demo.video where moduleType = 'G' and Type = %s and  modetype <> %s",(level,GrammarLabel,))
            GrammerMaterials = cursor.fetchall()

            cursor.execute("select video_name,actual_name,video_thumbnail from demo.video where moduleType = 'R' and Type = %s and  modetype <> %s",(level,ReadingLabel,))
            ReadingMaterials = cursor.fetchall()

            cursor.execute("select video_name,actual_name,video_thumbnail from demo.video where moduleType = 'C' and Type = %s and  modetype <> %s",(level,ComputerLabel,))
            ComputerMaterials = cursor.fetchall()

            cursor.execute("select video_name,actual_name,video_thumbnail from demo.video where moduleType = 'W' and Type = %s and  modetype <> %s",(level,WritingLabel,))
            WritingMaterials = cursor.fetchall()

            myFile = open('../Exp25/ML/static/app1/csv/tmp.csv', 'w')
            myFile.seek(0)
            myFile.truncate()
            data = []
            data.append(["Type","Seeking","Replay","Pauses"])
            while row is not None:

                VocabTotal = row[-24]
                GrammarTotal = row[-23]
                ReadingTotal = row[-22]
                ComputerTotal = row[-21]
                WritingTotal = row[-20]
                VideoTotal = row[-19]
                AudioTotal = row[-18]
                PPTTotal = row[-17]

                VideoSeeking = row[-33]
                VideoReplay = row[-31]
                VideoPause = row[-32]
                vd = ["Video",VideoSeeking,VideoReplay,VideoPause]
                data.append(vd)

                AudioSeeking = row[-30]
                AudioReplay = row[-28]
                AudioPause = row[-29]
                ad = ["Audio",AudioSeeking,AudioReplay,AudioPause]
                data.append(ad)

                PPTSeeking = row[-27]
                PPTReplay = row[-25]
                PPTPause = row[-26]
                pd = ["PPT",PPTSeeking,PPTReplay,PPTPause]
                data.append(pd)

                VocabLabel = row[-8]
                GrammarLabel = row[-7]
                ReadingLabel = row[-6]
                ComputerLabel = row[-5]
                WritingLabel = row[-4]



                with myFile:
                    writer = csv.writer(myFile)
                    writer.writerows(data)
                myFile.close()

                return render(request, 'e_learning/Userprofile.html',{"username":name,"VocabTotal":VocabTotal,        "GrammarTotal":GrammarTotal,"ReadingTotal":ReadingTotal,"ComputerTotal":ComputerTotal,"WritingTotal":WritingTotal,"RowVoc":RowVoc,"RowGra":RowGra,"RowRea":RowRea,"RowComp":RowComp,"RowWri":RowWri,"TopVoc":TopVoc[0],"TopGra":TopGra[0],"TopRea":TopRea[0],"TopComp":TopComp[0],"TopWri":TopWri[0],"VocabularyMaterials":VocabularyMaterials,"GrammerMaterials":GrammerMaterials,"ReadingMaterials":ReadingMaterials,"ComputerMaterials":ComputerMaterials,"WritingMaterials":WritingMaterials,"VocabLabel" :VocabLabel,"GrammarLabel" :GrammarLabel,"ReadingLabel" :ReadingLabel,"ComputerLabel" :ComputerLabel,"WritingLabel" :WritingLabel})
                #row = cursor.fetchone()
        except Error as e:
            print(e)
            return render(request, 'e_learning/Userprofile.html',{"username":user})

        finally:

            cursor.close()
            conn.close()


        #return render(request, 'e_learning/Userprofile.html',{"username":name,"data":row})
    else:
        return redirect('login')
