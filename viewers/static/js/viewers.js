$(document).ready(function() {
  var WEBSOCKET_URL = "ws://"+window.location.hostname+":10081/monobattles";
  
  var form_container = $('#verify_form_container');
  var verify_success = $('#verify_message');
  var signup = $('#submit_form_container');
  var monobattle_status = $('#monobattle_status');
  var websocket = null;
  
  $('#verify_form_container, #verify_message, #submit_form_container').hide();
  $('.loading_indicator').hide();
  
  if (is_jtv_verified) {
    verify_success.show();
    signup.show();
  }
  else {
    form_container.show();
  }
  
  $('#verify_form').submit(function() {
    var username = $.trim($(this).find('#id_username').val());
    var password = $.trim($(this).find('#id_password').val());
    var submit = $(this).find('input[type=submit]');
    var loading = $(this).find('.loading_indicator');
    
    if (username == '' || password == '') {
      $('#verify_error').html('Please fill out your username and password');
      return false;
    }
    
    loading.show();
    submit.attr('disabled', 'disabled');
    $.ajax($(this).attr('action'), {
      type: 'post',
      data: {
        'username': username,
        'password': password
      },
      dataType: 'json',
      success: function(data, status, xhr) {
        if (data.success) {
          form_container.hide();
          verify_success.show();
          signup.show();
        }
        else {
          $('#verify_error').html(data.message);
        }
      },
      complete: function(xhr, status) {
        submit.removeAttr('disabled');
        loading.hide();
      }
    });
    
    return false; 
  });
  
  $('#submit_form').submit(function() {
    var name = $.trim($(this).find('#id_sc2name').val());
    var code = $.trim($(this).find('#id_sc2code').val());
    var submit = $(this).find('input[type=submit]');
    var loading = $(this).find('.loading_indicator');
    
    if (name == '' || code == '') {
      $('#submit_message')
        .html('Please fill out your sc2 character name and code')
        .addClass('error_message');
      return false;
    }
    
    submit.attr('disabled', 'disabled');
    loading.show();
    $.ajax($(this).attr('action'), {
      type: 'post',
      data: {
        'sc2_name': name,
        'sc2_charcode': code
      },
      dataType: 'json',
      success: function(data, status, xhr) {
        if (data.success) {
          $('#submit_message')
            .html(data.message)
            .removeClass('error_message');
          setTimeout(function() {
            submit.removeAttr('disabled');
          }, 15000);
        }
        else {
          $('#submit_message')
            .html(data.message)
            .addClass('error_message');
          submit.removeAttr('disabled');
        }
      },
      complete: function(xhr, status) {
        loading.hide();
      }
    });
    
    return false;
  });
  
  var set_status = function(is_enabled) {
    if (is_enabled) {
        monobattle_status
          .addClass('enabled')
          .removeClass('disabled')
          .html('Monobattles are ON');
      }
      else {
        monobattle_status
          .addClass('disabled')
          .removeClass('enabled')
          .html('Monobattles are OFF');
      }
  }
  
  var connect = function() {
    try {
      websocket = new WebSocket(WEBSOCKET_URL);
    }
    catch (exception) {
      return;
    }
    
    websocket.onopen = function() {
      websocket.send(JSON.stringify({
        'connect': true
      }));
    }
    websocket.onmessage = function(event) {
      var json = $.parseJSON(event.data);
      if ('is_enabled' in json) {
        set_status(json.is_enabled);
      }
    }
    websocket.onerror = function() {
      alert('ERROR!');
    }
    websocket.onclose = function(event) {
      
    }
  }
  
  connect();
  set_status(monobattles_enabled);
});