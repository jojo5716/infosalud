/*
 * Info Salud 
 * 
 *
 *
 * Copyright (c) 2011, Jonathan Rodriguez 
 */
(function($){
    $.fn.jGetTwitter = function(user_options) {
        var default_settings = {
            "username" : 'inf_salud',
            "NoOfTweets" : 5,
            "ProfilePhoto" : true,
            "TweetTime" : true,
            "FollowerDisplay" : true,
            "TotalNoOfTweets" : true,
            "theme" : 'grey',
            "width" : 300
        };
        
        if(user_options){
            $.extend(default_settings, user_options);
        }
        
        var targetContainer = '#' + $(this).attr('id');
        var userName = default_settings['username'];
        var NoOfTweets = default_settings['NoOfTweets'];
        var profilePhoto = default_settings['ProfilePhoto'];
        var followerDisplay = default_settings['FollowerDisplay'];
        var TotalNoOfTweets = default_settings['TotalNoOfTweets'];
        var tweetTime = default_settings['TweetTime'];
        var theme = default_settings['theme'];
        var width = default_settings['width'];
        var tweet;
        var info;
        
        var url = 'http://api.twitter.com/1/statuses/user_timeline/' + userName + '.json?callback=?';
        
        $.getJSON(url, function (tweets) {
          
            
            for (var i = 0; i < NoOfTweets; i++) {   
                tweet = "<div class='tweetContainer'>";
                if(profilePhoto == true) {
                    tweet += "<div class='profile_img'><img src='" + tweets[i].user.profile_image_url + "' /></div>";
                }
                tweet += "<div>" + tweets[i].text + "</div>";
                if(tweetTime == true) {
                    tweet += "<div class='timeago'>" + timeAgo(tweets[i].created_at) + "</div>";
                }
                tweet += "<div class='no_float'></div>";
                tweet += "</div>";
                
                $(targetContainer).append(tweet).fadeIn(1000);
            }
            
            $(targetContainer).prepend(info);
            themeColor(theme);
        });
        
        //function to display time in timeago format
        function timeAgo(d) {
            //to get unix timestamp
            var currentDate = Math.round(+new Date()/1000);
            var tweetDate = Math.round(+new Date(d)/1000); 
            
            var diffTime = currentDate - tweetDate;
            
            if (diffTime < 59) return 'less than a minute ago';
            else if(diffTime > 59 && diffTime < 120) return 'about a minute ago';
            else if(diffTime >= 121 && diffTime <= 3600) return (parseInt(diffTime / 60)).toString() + ' minutes ago';
            else if(diffTime > 3600 && diffTime < 7200) return '1 hour ago';
            else if(diffTime > 7200 && diffTime < 86400) return (parseInt(diffTime / 3600)).toString() + ' hours ago';
            else if(diffTime > 86400 && diffTime < 172800) return '1 day ago';
            else if(diffTime > 172800 && diffTime < 604800) return (parseInt(diffTime / 86400)).toString() + ' days ago';
            else if(diffTime > 604800 && diffTime < 12089600) return '1 week ago';
            else if(diffTime > 12089600 && diffTime < 2630880) return (parseInt(diffTime / 604800)).toString() + ' weeks ago';
            else if(diffTime > 2630880 && diffTime < 5261760) return '1 month ago';
            else if(diffTime > 5261760 && diffTime < 31570560) return (parseInt(diffTime / 2630880)).toString() + ' months ago';
            else if(diffTime > 31570560 && diffTime < 63141120) return '1 year ago';
            else return (parseInt(diffTime / 31570560)).toString() + ' years ago';
        }
        
        //function to add CSS styles on div tags
        function addStyles() {
            $('.profile_img').css('height','100%')
                             .css('position','relative')
                             .css('margin-right','5px')
                             .css('float','left');
            
            $('.tweetContainer').css('padding','5px')
                                .css('width',width)
                                .css('margin-bottom','3px')
                                .css('font-size','16px')
                                .css('border-radius','5px')
                                
                                .css('background','#F5F5F5')
                                .css('text-shadow','0 1px 1px white');
                                
           $('.tweetContainer ul').css('list-style','none')
                                  .css('padding','5px')
                                  .css('margin','0 0 0px 0px')
                                  .css('font-weight','bold')
                                  .css('color','#333333')
                                  .css('font-size','11px');
                                  
            $('.tweetContainer ul li:first-child').css('font-size','18px');
            
            $('.timeago').css('color','#333333')
                         .css('font-size','11px')
                         .css('font-style','italic');
            
            $('.no_float').css('clear','both');
        }
        
        //theme for jGetTwitter.
        function themeColor(theme) {
            var gradientBg;
            var borderBg;
            
            addStyles();
            
     
          
          
        
            
          
            
           
            $('.tweetContainer').css("background",gradientBg)
                                .css("border",borderBg);
        } //end of function
    }
})(jQuery);