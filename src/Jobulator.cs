using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;

namespace jobulator {
	public class Jobulator {

		public Jobulator () {}

		public static void Main() {

			var d = new Driver ();
			d.GoTo ("indeed.ca");
			//d.PrintCurrentPage ();
			d.Dispose ();

			GUI g = new GUI ("jobulator");
			g.Start ();

			//GenerateWordList ();

			/*
			foreach (Job j in Job.getJobsFrom("html", 500)) {
				//Console.WriteLine(j.Get("application_deadline"));
                if(JobChooser.Test(j)){
					CoverLetter.Generate (j);
				}
			}*/

			//StartGUI ();
		}
		public static void GenerateWordList(List<Job> jobs){
			var wordFrequency = new Dictionary<string, int> ();
			var list = new List<KeyValuePair<string, int>> ();

			foreach(Job j in jobs){
				string[] words = j.Get("job_requirements")
					.Split(new string[] { Environment.NewLine, " ", ".", ","  }, StringSplitOptions.RemoveEmptyEntries);
				foreach (string word in words) {
					var w = Regex.Match(word, @"[A-Za-z0-9\-\']+").Groups[0].Value.ToLower();
					if (wordFrequency.ContainsKey (w))
						wordFrequency [w] = (wordFrequency [w]) + 1;
					else
						wordFrequency.Add (w, 1);
				}
			}
			foreach (KeyValuePair<string, int> kvp in wordFrequency)
				list.Add (kvp);
			list.Sort(delegate(KeyValuePair<string, int> x, KeyValuePair<string, int> y){
				return y.Value.CompareTo(x.Value);
			});
			var output = "";
			foreach(KeyValuePair<string, int> kvp in list) {
				output += kvp.Key + " " + kvp.Value + "<br>" + Environment.NewLine;
			}
			FileHandler.Write (output, "wordlist.txt");
		}
	}
}

