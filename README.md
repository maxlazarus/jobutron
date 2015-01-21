# jobulator
Utility developed for scraping employment postings

This application has 2 different parts (which I hope to integrate soon)

  - python code: utility to rip job postings into local html files
    - usage: in jobulator/src python web_functions.py
    - dependencies: will try to install selenium with pip if not present
      - phantomjs ghostdriver executables should already be present
    
  - c# code: utility to extract key information from the html and format as json
      - also tools to automatically generate cover letters and save as .docx
    - usage: vanilla c# (for now), compile and run jobulator.cs, I'm using mono
      - so there may be key references missing if you are compiling it by another method
    - dependencies: Novacode should already be included as package already
    
  - if you have difficulties contact me at max@theprogramminglub.com, I appreciate the response

Could not be possible without Selenium Webdriver
  - http://docs.seleniumhq.org/projects/webdriver/

and PhantomJS
  - http://phantomjs.org/
  
and Novacode docx library for C#
  - https://docx.codeplex.com/
