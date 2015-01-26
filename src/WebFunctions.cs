using System;
using OpenQA.Selenium;
using OpenQA.Selenium.PhantomJS;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Chrome;
using System.IO;

namespace jobulator {
	public class WebFunctions {
		public WebFunctions () {
		}

		public static void Init() {
			IWebDriver driver = new ChromeDriver (@"/Users/maxlazar/github/jobulator/bin/");
			driver.Navigate ().GoToUrl ("http://www.maximixam.com");
			var content = driver.PageSource;
			Console.Write (content);
		}
	}
}

