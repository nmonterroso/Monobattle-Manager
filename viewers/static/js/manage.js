$(document).ready(function() {
  var action = 'enable';
  var action_button = $('#action');
  var next_action = $('#next_action');
  var loading = $('#loading_indicator');
  var signups = $('#monobattle_signups');
  
  action_button.click(function() {
    loading.show();
    $.ajax('/manage-action', {
      type: 'post',
      dataType: 'json',
      data: {
        'action': action
      },
      success: function(data, stat, xhr) {
        signups_enabled = !signups_enabled;
        set_status();
        show_message(data.message);
        
        if (!signups_enabled) {
          show_submissions(data.submissions)
        }
      },
      complete: function(xhr, stat) {
        loading.hide();
      }
    });
  });
  
  var show_submissions = function(submissions) {
    signups.html('');
    
    var html = "<table><tr><th>sc2 name</th><th>sc2 code</th><th></th></tr>";
    $.each(submissions, function(i, submission) {
      html += "<tr><td>"+submission.name+"</td><td>"+submission.code+"</td><td>"+submission.time+"</td></tr>";
    });
    html += "</table>";
    
    signups.html(html);
    show_message("<strong>"+submissions.length+"</strong> submissions!")
  }
  
  var set_status = function() {
    if (signups_enabled) {
      action = 'disable';
      next_action.html('disable');
      action_button.html('disable');
    }
    else {
      action = 'enable';
      next_action.html('enable');
      action_button.html('enable');
    }
  }
  
  var show_message = function(message) {
    $('#message').html(message);
  }
  
  loading.hide();
  set_status();
})