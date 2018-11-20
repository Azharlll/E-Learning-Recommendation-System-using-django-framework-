/*! @name videojs-extractor @version 0.0.0 @license Apache-2.0 */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('video.js')) :
  typeof define === 'function' && define.amd ? define(['video.js'], factory) :
  (global.videojsExtractor = factory(global.videojs));
}(this, (function (videojs) { 'use strict';

  videojs = videojs && videojs.hasOwnProperty('default') ? videojs['default'] : videojs;

  var version = "0.0.0";

  // Default options for the plugin.
  var defaults = {};

  // Cross-compatibility for Video.js 5 and 6.
  var registerPlugin = videojs.registerPlugin || videojs.plugin;
  // const dom = videojs.dom || videojs;

  /**
   * Function to invoke when the player is ready.
   *
   * This is a great place for your plugin to initialize itself. When this
   * function is called, the player will have its DOM and child components
   * in place.
   *
   * @function onPlayerReady
   * @param    {Player} player
   *           A Video.js player object.
   *
   * @param    {Object} [options={}]
   *           A plain object containing options for the plugin.
   */
  var onPlayerReady = function onPlayerReady(player, options) {
    player.addClass('vjs-videojs-extractor');

    var previousTime = 0;
    var currentTime = 0;
    var pausecount = 0;
    var seekcount = 0;
    var replaycount = 0;
    var seekStart = null;

    player.on('timeupdate', function () {
      previousTime = currentTime;
      currentTime = player.currentTime();
    });
    player.on('seeking', function () {
      if (seekStart === null) {
        seekStart = previousTime;
      }
    });

    player.on('seeked', function () {

      seekcount += 1;
      var whereYouAt = player.currentTime();

      //(imp)console.log('seeked from', seekStart, 'to', currentTime, '; delta:', currentTime - seekStart);
      //(imp)console.log('User Seeked',seekcount,' times.')
      seekStart = null;

      if (-Math.floor(seekStart) === Math.floor(currentTime - seekStart)) {
        replaycount += 1;
        seekcount -= 1;
        pausecount -= 1;
        //(imp)console.log('User Replayed ',replaycount,' times.')
      }
    });

    player.on('pause', function () {
      var whereYouAt = player.currentTime();

      if (!player.seeking()) {
        pausecount += 1;
        //(imp)pausedata.push({key : pausecount ,value : whereYouAt});
        //(imp)console.log('User has paued the video.');
        //(imp)console.log('User paused',pausecount,' times.');
      }
    });

    player.on('ended', function () {
      console.log(pausecount, seekcount, replaycount);


    });

    function savedata() {
      var data = new Object();
      data.pausecount = JSON.stringify(pausecount);
      data.seekcount = JSON.stringify(seekcount);
      data.replaycount = JSON.stringify(replaycount);
      //   data.pausedata = JSON.stringify(pausedata);
      // data.seekdata = JSON.stringify(seekdata);
      return data;




    }
    //document.getElementById("id_seeking").value=seekcount;
    //document.getElementById("id_pauses").value=pausecount;
    //document.getElementById("id_replaycount").value=replaycount;

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  console.log(csrftoken);
  //  var da = {csrfmiddlewaretoken: "{{ csrf_token }}", d : savedata()};
  /*  var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
    console.log(this);
    var csrfToken = this.getResponseHeader('x-csrf-token');
    if(xhttp.readyState == 4){
        console.log(csrfToken);
        xhttp.open('POST', '/api/1.0/create');
        xhttp.setRequestHeader('x-csrf-token', this.getResponseHeader('x-csrf-token'));
        xhttp.onreadystatechange = function () {
            console.log("call 2");
            console.log(this.responseText);
        };
        xhttp.send(savedata());
    }
};
xhttp.send();*/
//var res = null;
/*var tryout = new XMLHttpRequest();
console.log(tryout.readyState);

  //var csrfToken = tryout.getResponseHeader('x-csrf-token');

  tryout.open('GET', '/getdata/', true);
  tryout.setRequestHeader('x-csrf-token',getCookie('csrftoken'));
  tryout.setRequestHeader("Content-Type", "application/json; charset=utf-8");
  tryout.setRequestHeader("Accept", "application/json");

  tryout.send(JSON.stringify(savedata()));*/



    //xhttp.open("POST", "http://127.0.0.1:8000/getdata/", true);
    //xhttp.send(da);


    var user= document.getElementById("author_id").value;
    var paths= document.getElementById("paths").value;
    console.log(user,paths)

    window.addEventListener("beforeunload", function (e) {
      //var confirmationMessage = "\o/";
      //e.returnValue = confirmationMessage;

      $.ajax({
        url: '/ajax/',
        data: {
          'user': user,
          'pausecount': pausecount,
          'seekcount': seekcount,
          'replaycount': replaycount,
          'paths': paths,
        },
        dataType: 'json',
        success: function (data) {
          if (data.is_taken) {
          console.log("Gone to otherside.");
          }
        }
      });
      if (e.returnValue) {
        //savedata();

      }    //return confirmationMessage; // Gecko, WebKit, Chrome <34
    });
  };

  /**
   * A video.js plugin.
   *
   * In the plugin function, the value of `this` is a video.js `Player`
   * instance. You cannot rely on the player being in a "ready" state here,
   * depending on how the plugin is invoked. This may or may not be important
   * to you; if not, remove the wait for "ready"!
   *
   * @function extractor
   * @param    {Object} [options={}]
   *           An object of options left to the plugin author to define.
   */
  var extractor = function extractor(options) {
    var _this = this;

    this.ready(function () {
      onPlayerReady(_this, videojs.mergeOptions(defaults, options));
    });
  };

  // Register the plugin with video.js.
  registerPlugin('extractor', extractor);

  // Include the version number.
  extractor.VERSION = version;

  return extractor;

})));
