/***
 Target: Cisco Spark specific integration
 Version: 0.1
 Date: 2017/01/18
 Mail: guillain@gmail.com
 Copyright 2017 GPL - Guillain
***/

/* dashboard function */

var dashboardArray = function(val){
              // sql req: session['grp'], s.sid, s.name, u.uid, s.birthday, s.timestamp, s.severity, s.status
              //        :              0,      1,     2,     3,          4,           5,          6,        7
              tmpbuffer = ''; 
              if (val['0']['0'] == 'admin') {  
                tmpbuffer = '<th>UID</th>'; 
              }

              buffer  = '<table class="tblCenter">';
              buffer += '  <tr><th>Name</th>'+tmpbuffer+'<th>Update</th><th>Status</th><th>Actions</th></tr>';
              for(var i=0; i < val.length; i++){
                  buffer += '<tr>';
                  buffer += '<td class="tblLeft">'+val[i]['2']+'</td>';

                  if (val[i]['0'] == 'admin') { buffer += '<td class="tblLeft">'+val[i]['3']+'</td>'; }

                  //buffer += '<td class="tblLeft">'+val[i]['4']+'</td>';
                  buffer += '<td class="tblLeft">'+val[i]['5']+'</td>';
                  buffer += '<td class="tblLeft">'+val[i]['6']+'</td>';
                  buffer += '<td class="tblLeft">';
                  if (val[i]['7'] != 'close') {
                    buffer += '<form action="view" method="POST" id="view'+val[i]['1']+'">';
                    buffer += '  <a href="#" onclick=\'document.getElementById("view'+val[i]['1']+'").submit()\'>View</a>';
                    buffer += '  <input type="hidden" name="sid" value="'+val[i]['1']+'"/>';
                    buffer += '  <input type="hidden" name="sname" value="'+val[i]['2']+'"/>';
                    buffer += '</form>';

                    buffer += '<form action="update" method="POST" id="update'+val[i]['1']+'">';
                    buffer += '  <a href="#" onclick=\'document.getElementById("update'+val[i]['1']+'").submit()\'>Update</a>';
                    buffer += '  <input type="hidden" name="sid" value="'+val[i]['1']+'"/>';
                    buffer += '  <input type="hidden" name="sname" value="'+val[i]['2']+'"/>';
                    buffer += '</form>';
                  }
                  buffer += '<form action="dump" method="POST" id="dump'+val[i]['1']+'">';
                  buffer += '  <a href="#" onclick=\'document.getElementById("dump'+val[i]['1']+'").submit()\'>Dump</a>';
                  buffer += '  <input type="hidden" name="sid" value="'+val[i]['1']+'"/>';
                  buffer += '  <input type="hidden" name="sname" value="'+val[i]['2']+'"/>';
                  buffer += '</form>';

                  if (val[i]['0'] == 'admin') {
                    if (val[i]['7'] != 'close') {
                      buffer += '<form action="close" method="POST" id="close'+val[i]['1']+'">';
                      buffer += '  <a href="#" onclick=\'document.getElementById("close'+val[i]['1']+'").submit()\'>Close</a>';
                      buffer += '  <input type="hidden" name="sid" value="'+val[i]['1']+'"/>';
                      buffer += '  <input type="hidden" name="sname" value="'+val[i]['2']+'"/>';
                      buffer += '</form>';
                    }
                  }
                  buffer += '</td></tr>';
              }
              buffer += '</table>';

              return buffer;
}

  $(function() {
    $('a#dashboardSub').bind('click', function() {
      $.ajax({
        url: '/dashboard',
        data: $('form').serialize(),
        type: 'POST',
        success: function(data) {
          console.log(data);
          var buffer="";
          $.each(data, function(index, val){
            if (val.length == 0) {
              $('#dashboardRes').html('<li>No space found</li>');
            } else {
              $('#dashboardRes').html(dashboardArray(val));
            }
          });
        },
        error: function(error) {
          console.log(error);
          $("#result").text(error);
        }
      });
    });
  });

/* updateSub click */
  $(function() {
    $('a#updateSub').bind('click', function() {
        $.ajax({
            url: '/updateSub',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* newSub click */
  $(function() {
    $('a#newSub').bind('click', function() {
        $.ajax({
            url: '/newSub',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* userupdate click */
  $(function() {
    $('a#userupdate').bind('click', function() {
        $.ajax({
            url: '/userupdate',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });


/*  popup confirmation */
function getConfirm(){
    if(confirm('Are you sure you want to disable this button?') == true) {
        return true;
    }
    else {
        return false;
    }
}

/* get session ID */
var getSessionParam = function getSessionParam(sParam){
    var re = new RegExp('/'+sParam+'=[^;]+/');
    var jsId = document.cookie.match(re);
    if(jsId != null) {
        if (jsId instanceof Array)
            jsId = jsId[0].substring(11);
        else
            jsId = jsId.substring(11);
    }
    return jsId;
}

/* get Url parameters */
var getUrlParam = function getUrlParam(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

/* display additionnal info when onmouse */
function onmouseoveragent(el) {
    var hint = el.querySelector("div.hideme");
    hint.style.display = 'block';

    hint.style.top = Math.max(el.offsetTop - hint.offsetHeight,0) + "px";
    hint.style.left = el.offsetLeft + "px";
};
function onmouseoutagent(el) {
    var hint = el.querySelector("div.hideme");
    hint.style.display = 'none';
}

/* json to list function */
function jsonToList(data) {    
    if (typeof(data) == 'object') {        
        var ul = $('<ul>');
        for (var i in data) {            
            ul.append($('<li>').text(i).append(jsonToList(data[i])));         
        }        
        return ul;
    } else {       
        var textNode = document.createTextNode(' => ' + data);
        return textNode;
    }
}

// implement JSON.stringify serialization
function jsonToString(obj){
    var t = typeof (obj);
    if (t != "object" || obj === null) {
        // simple data type
        if (t == "string") obj = '"'+obj+'"';
        return String(obj);
    }
    else {
        // recurse array or object
        var n, v, json = [], arr = (obj && obj.constructor == Array);
        for (n in obj) {
            v = obj[n]; t = typeof(v);
            if (t == "string") v = '"'+v+'"';
            else if (t == "object" && v !== null) v = JSON.stringify(v);
            json.push((arr ? "" : '"' + n + '":') + String(v));
        }
        return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
    }
};

