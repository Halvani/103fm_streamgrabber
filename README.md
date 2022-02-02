# 103fm StreamGrabber
This small script downloads episodes of arbitrary radio shows from the 103fm website: https://103fm.maariv.co.il

Currently a dictionary of five radio shows is predefined, which can be extended easily. <br>
For this, you first have to select your favorite radio show under https://103fm.maariv.co.il/programs 

For example, the radio show of Didi Lokali ("דידי-לוקאלי") can be found under the URL: 
https://103fm.maariv.co.il/program/%D7%93%D7%99%D7%93%D7%99-%D7%9C%D7%95%D7%A7%D7%90%D7%9C%D7%99-%D7%93%D7%99%D7%93%D7%99-%D7%94%D7%A8%D7%A8%D7%99.aspx

Within this URL you must afterwards copy the URL of the complete epidodes ("תוכניות מלאות"):<br> 
https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=EG 
<br>
This URL needs to be added to the predefined dictionary. 

To download the shows, all you have to do is specify the destination folder. <br>
After that you just need to run the script either from the command line or by double-clicking it in your desired file browser. 

Enjoy listening!


# Dependencies:
beautifulsoup4==4.10.0 <br>
requests==2.27.1 <br>
tqdm==4.62.3 <br>
