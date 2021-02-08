// EPA's Core JS file, vOneEPA Web
// 23 Mar 2012: Added Twitter
// 20 June 2012: Added Google Analytics
// 08 Jan 2013: More robust GA tracking
// 08 Feb 2013: Sending GA data to GSA
// 01 May 2013: Saving body classes
// 13 Aug 2013: Remove body class tracking for GA
// Questions? hessling.michael@epa.gov
var epaCore = {
  //Date related functions
  takeYear: function(theDate) { var x = theDate.getYear(); var y = x % 100; y += (y < 38) ? 2000 : 1900; return y; },
  //Bookmarklet popup
  postPopUp: function(url, name, params) { var win = window.open(url, name, params); }
};

// Start Google Analytics- 12-14-12
var _gaq = _gaq || [];

// Use jQuery via jQuery(...); no conflict
jQuery(document).ready(function() {

function loadtracking() {

/*
 * Get Root Domain- Used for Google Analytics _setDomainName & _addIgnoredRef
 */

var epaGA_hostName= window.location.hostname;
var epaGA_hostArray= epaGA_hostName.split('.').slice(-2);
var epaGA_hostDomain= epaGA_hostArray.join('.').toLowerCase();

/*
 * Get Google Analytics Visitor Cookie
 */

function getCookie(c_name) {
var i,x,y,ARRcookies=document.cookie.split(";");
for (i=0;i<ARRcookies.length;i++)
  {
  x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
  y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
  x=x.replace(/^\s+|\s+$/g,"");
  if (x==c_name)
    {
    return unescape(y);
    }
  }
}

var epaGA_visitorIdCookie=getCookie("__utma");

if (epaGA_visitorIdCookie!=null && epaGA_visitorIdCookie!="") {
 var epaGA_visitorIDCookieSplit= epaGA_visitorIdCookie.split(".");
 var epaGA_gaVisitorID= (epaGA_visitorIDCookieSplit[1]);
}
else {
 epaGA_gaVisitorID="one and done visitor"
}

/* START For Cross Domain Tracking Use Visitor ID from __utma query param instead of cookie */

function getQuerystring(key, default_) {
  if (default_==null) default_="";
  key = key.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regex = new RegExp("[\\?&]"+key+"=([^&#]*)");
  var qs = regex.exec(window.location.href);
  if(qs == null)
    return default_;
  else
    return qs[1];
}

if(window.location.href.indexOf('__utma') > 1){
	epaGA_gaVisitorID = getQuerystring('__utma').split('.')[1];
}//if
else{
	//nothing
}//else

/* END For Cross Domain Tracking Use Visitor ID from __utma query param instead of cookie  */

// Page Level Google Analytics Code

 _gaq.push(['_setAccount', 'UA-32633028-1']);
 _gaq.push(['_setDomainName', epaGA_hostDomain]);
 _gaq.push(['_addIgnoredRef', epaGA_hostDomain]);
 _gaq.push(['_setAllowLinker', true]);
 _gaq.push(['_setCustomVar',1,'visitor id',epaGA_gaVisitorID,1]);

 _gaq.push(['_trackPageview']);

 _gaq.push(['GSA._setAccount', 'UA-33523145-1']); // Parallel tracking to GSA, UA-33523145-1
 _gaq.push(['GSA._setDomainName', epaGA_hostDomain]); // Parallel tracking to GSA
 _gaq.push(['GSA._addIgnoredRef', epaGA_hostDomain]);  // Parallel tracking to GSA
 _gaq.push(['GSA._setAllowLinker', true]);  // Parallel tracking to GSA - will use referring site's cookies sent in URL
 _gaq.push(['GSA._setCustomVar', 3, 'Agency', 'EPA', 3]); // Page level variable sent only to GSA account
 _gaq.push(['GSA._setCustomVar', 4, 'Sub-Agency', 'EPA - ' + epaGA_hostName, 3]); // Page level variable sent only to GSA account
 _gaq.push(['GSA._setCustomVar', 5, 'Code Ver', 'EPA 1.0 121211', 3]); // Page level variable sent only to GSA account
 _gaq.push(['GSA._trackPageview']); // Parallel tracking to GSA

(function() {

 var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
 ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
 var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);

})();

/************START Google Analytics jQuery Download & External Link & Mailto & Cross Domain Tracking******************/

	//Specify Filetypes Tracked
        var filetypes = /\.(zip|exe|pdf|doc*|xls*|ppt*|mp3)$/i;

	//Specify Cross Domains Tracked
		var domains = /(epa.gov|epa-otis.gov|epa-echo.gov|energystar.gov|enviroflash.info|airnow.gov|urbanwaters.gov|relocatefeds.gov|lab21century.gov|supportportal.com)/i;

		var crossExclude = /(http:\/\/oaspub.epa.gov\/enviro\/fii_query_dtl.disp_program_facility|http:\/\/iaspub.epa.gov\/enviro\/tsca.get_chem_info|http:\/\/iaspub.epa.gov\/enviro\/ICIS_DETAIL_REPORTS_NPDESID.icis_tst|http:\/\/oaspub.epa.gov\/enviro\/tris_control.tris_print|http:\/\/www.epa.gov\/myenv\/myenview2.html|http:\/\/www.epa.gov\/emefdata\/em4ef.html|http:\/\/nepassisttool.epa.gov\/nepassist\/nepamap.aspx|http:\/\/nepassist.epa.gov\/nepave\/nepamap.aspx|cfpub.epa.gov|yosemite.epa.gov|iaspub.epa.gov|oaspub.epa.gov|ofmpub.epa.gov|watersgeo.epa.gov|cfpub2.epa.gov|cumulis.epa.gov|cfpub1.epa.gov|actor.epa.gov|nepis.epa.gov|yosemite1.epa.gov|ofmext.epa.gov|epamap32.epa.gov|gispub2.epa.gov|gispub6.epa.gov|epamap10.epa.gov|epamap21.epa.gov|maps6.epa.gov|ghgdata.epa.gov\/ghgp\/main.do)/i;

		var baseHref = '';
        if (jQuery('base').attr('href') != undefined)
            baseHref = jQuery('base').attr('href');
        jQuery('a').each(function() {
            var href = jQuery(this).attr('href');

	//Cross Domain Tracking

			if (href && (href.match(domains)) && (href.indexOf(epaGA_hostDomain) == -1 ) && (!href.match(crossExclude))) {
			 jQuery(this).click(function() {
                    var extLink = href.replace(/^https?\:\/\//i, '');
                    _gaq.push(['_trackEvent', 'crossDomain', 'Link Click', extLink]);
					_gaq.push(['GSA._trackEvent', 'crossDomain', 'Link Click', extLink]);  // Parallel tracking to GSA
					_gaq.push(['_setAllowLinker', true]);
					 if (this.target == '_blank') {
										window.open(_gat._getTrackers()[0]._getLinkerUrl(this.href));
									} else {
										_gaq.push(['_link', this.href]);
									}
								return false;
                });
			}

		//Download Link Tracking

          	else if (href && href.match(filetypes)) {
                jQuery(this).click(function() {
                    var extension = (/[.]/.exec(href)) ? /[^.]+$/.exec(href) : undefined;
                    var filePath = href;
                    _gaq.push(['_trackEvent', 'Download',extension+ ' Click', filePath]);
					_gaq.push(['GSA._trackEvent', 'Download',extension+ ' Click', filePath]);  // Parallel tracking to GSA
                    if (jQuery(this).attr('target').toLowerCase() != '_blank') {
                        setTimeout(function() { location.href = baseHref + href; }, 200);
                        return false;
                    }
                });
            }

		  //Mailto Link Tracking

            else if (href && href.match(/^mailto\:/i)) {
                jQuery(this).click(function() {
                    var mailLink = href.replace(/^mailto\:/i, '');
                    _gaq.push(['_trackEvent', 'Email', 'Link Click', mailLink]);
					_gaq.push(['GSA._trackEvent', 'Email', 'Link Click', mailLink]);   // Parallel tracking to GSA
					setTimeout(function() { location.href = href; }, 150);
					return false;
                });
            }

			//External Link Tracking

           else if (href && (href.match(/^https?\:/i)) && (href.indexOf(epaGA_hostDomain) == -1 )) {
                jQuery(this).click(function() {
                    var extLink = href.replace(/^https?\:\/\//i, '');
                    _gaq.push(['_trackEvent', 'External', 'Link Click', extLink]);
					_gaq.push(['GSA._trackEvent', 'External', 'Link Click', extLink]);   // Parallel tracking to GSA
                    if (jQuery(this).attr('target') != undefined && jQuery(this).attr('target').toLowerCase() != '_blank') {
                        setTimeout(function() { location.href = href; }, 150);
                        return false;
                    }
                });
            }
        });

/************START Google Analytics jQuery Download & External Link & Mailto & Cross Domain Tracking******************/

// End Google Analytics
}

loadtracking();


  //Load Notice Script
  var ns = document.createElement('script');
  ns.async;
  ns.src = 'http://www.epa.gov/epahome/notice.js';
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(ns, s);

  //Load the ForeSee ACSI Survey code
  var fs = document.createElement('script');
  fs.async;
  fs.src = 'http://www.epa.gov/epafiles/js/third-party/foresee/foresee-trigger.js';
  //fs.src = 'http://www.epa.gov/epafiles/js/third-party/foresee/foresee-alive.js';
  s.parentNode.insertBefore(fs, s);

  //Load the Crazy Egg code
  //var ces = document.createElement('script');
  //ces.async;
  //ces.src = 'http://dnn506yrbagrg.cloudfront.net/pages/scripts/0005/9240.js';
  //s.parentNode.insertBefore(ces, s);

  //Search Autosuggest
	var sb = jQuery("#searchbox");
	if (sb[0]) {
	  sb.autocomplete("/autocomplete",{minChars:2,delay:200,matchSubset:false,selectFirst:false}).result(function (event, data, formatted) {
	    jQuery('#EPAsearch').submit();
	  });
	}

  //Stripe all tables with class="zebra"
	var t = jQuery('table.zebra tr:even');
	if (t[0]) { t.addClass('tint'); }

  //Date last modified
  if (document.lastModified == "") { var d = new Date(); }
  else { var d = new Date(document.lastModified); }
  var updated = document.createElement('p'); updated.id = 'date';
  updated.appendChild(document.createTextNode('Last updated on ' + d.toLocaleDateString()));
  var f = document.getElementById('footer');
  f.appendChild(updated);
  //Page URL
  var page_URL = document.createElement('p'); page_URL.id = 'url';
  page_URL.appendChild(document.createTextNode(window.location.href));
  f.appendChild(page_URL);

  //NEW! icon
	var x = new Date(); var today = new Date(x.toGMTString());
	var now = (Date.UTC(epaCore.takeYear(today),today.getMonth(),today.getDate(),0,0,0))/86400000;
	$("ins").each(function(i) {
	  var a = $(this).attr('datetime'); var b = a.split('-');
	  var posted = (Date.UTC(b[0],b[1],b[2],0,0,0))/86400000;
	  var time_left = posted - (now + 1);
	  if (time_left < 31  &&  time_left > 0) {
	    $(this).prepend("<img src='http://www.epa.gov/epafiles/images/new-en.gif' alt='New!' width='34' height='16'/>");
	  }
	});

  // Bookmarklet
	jQuery('#content').append('<ul id="share"><li><a href="#area">Share</a></li></ul>');
	var bookmarkList = '<ul><li class="facebook"><a href="#area" title="facebook">Facebook</a></li><li class="reddit"><a href="#area" title="reddit">reddit</a></li><li class="twitter"><a href="#area" title="twitter">Twitter</a></li><li class="whatisthis"><a href="#area" title="whatisthis">What is this?</a></li></ul>';
	jQuery('#share li').append(bookmarkList).hover(function() {jQuery(this).addClass("on");}, function() {jQuery(this).removeClass("on");});

	jQuery("#share li ul li a").click(function () {
	  var site = jQuery(this).attr('title');
	  var popURL = encodeURIComponent(window.location.href);
	  var title = encodeURIComponent(document.title);
	  switch (site) {
	    case "facebook": _gaq.push(['_trackSocial', 'facebook', 'share click', popURL]); epaCore.postPopUp('http://www.facebook.com/sharer.php?u='+popURL+'&t='+title, 'facebook', 'height=436,width=646,scrollbars=yes,resizable=yes'); break;
	    case "reddit": _gaq.push(['_trackSocial', 'reddit', 'share click', popURL]); epaCore.postPopUp('http://www.reddit.com/submit?url='+popURL, 'reddit', 'height=450,width=650,scrollbars=yes,resizable=yes'); break;
	    case "twitter": _gaq.push(['_trackSocial', 'twitter', 'share click', popURL]); epaCore.postPopUp('https://twitter.com/share?text='+title+'&url='+popURL+'&via=EPA&count=none&lang=en', 'twitter', 'height=375,width=550,scrollbars=yes,resizable=yes'); break;
	    case "whatisthis": setTimeout('window.location = "http://www.epa.gov/epahome/bookmarks.html"', 150); _gaq.push(['_trackSocial', 'what is this', 'what is this click', popURL]); break;
	  }
	});

});
