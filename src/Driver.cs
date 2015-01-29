using System;
using OpenQA.Selenium;
using OpenQA.Selenium.PhantomJS;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Chrome;
using System.IO;

namespace jobulator {
	public class Driver {
		IWebDriver driver;

		public Driver () {
			driver = new ChromeDriver (FileHandler.basePath + @"bin");
		}

		public void GoTo(String site) {
			driver.Navigate ().GoToUrl (@"http://www." + site);
		}
		public void SaveCurrentPageAs(String name) {
			FileHandler.Write(driver.PageSource, name);
		}
		public void PrintCurrentPage() {
			Console.Write (driver.PageSource);
		}
		public void Dispose() {
			driver.Dispose ();
		}
	}
}

