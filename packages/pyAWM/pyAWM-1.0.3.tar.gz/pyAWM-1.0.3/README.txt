Functions usage in this module:

1) users_manual() // to see how to use this module

2) add_driver_path(chrome_driver_path) //chrome_driver_path is absolute path to chromedriver.exe

3) scan_QR_Code() // to scan QR code

4) set_media_loading_time(secs) // to edit alloted upload time.(units of secs is seconds)

5) send_whatsapp_msg(["contact_1","contact_2"],"hello",1,16,0) 
	
	//first parameter is list of contact or group names.
	//second parameter is message that you want to send.
	//third parameter is number of times you want to send message to each participant.
	//fourth parameter is hour in 24 hr clock.
	//fifth parameter is minutes.

6) send_whatsapp_files(["contact_1","contact_2",...],["path_to_file_1","path_to_file_2", ...],16,0) //to send multiple documents

7) send_whatsapp_media(["contact_1","contact_2", ...],["path_to_file_1","path_to_file_2", ...],"message you want to send for this photo or video",16,0) //to send photo or video with a message