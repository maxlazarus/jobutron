using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using Gtk;

namespace jobulator {
	public class Jobulator {

		public Jobulator () {}

		public static void Main() {
		
			/*
			var l1 = getJobsFrom ("html", 500);
			foreach (Job j in l1)
				j.WriteJSON ();
				*/
			var jobs = getJobsFrom ("json", 500 );

			//GenerateWordList ();

			foreach (Job j in jobs) {
				//Console.WriteLine(j.Get("application_deadline"));
				if (
					(
						j.Get ("job_location").ToLower().Contains ("vancouver") |
						j.Get ("job_location").ToLower().Contains ("burnaby") |
						j.Get ("job_location").ToLower().Contains ("richmond")
					) && (
						j.Get("application_deadline").ToLower().Contains(@"jan 20")
					)
				) {
					Console.WriteLine ("Generating cover letter for position " + j.Get ("id"));
					CoverLetter cl = new CoverLetter (j);
					cl.printDOCX ();
				}
			}

			//Console.WriteLine ("# of html files = "l1.Count + ", # of JSON files = " + l2.Count);

			//StartGUI ();
		}
		public static List<Job> getJobsFrom(string fileType, int limit) {
			var jobList = new List<Job> ();

			int i = 1;
			var jobs = FileHandler.getFileNames (fileType);
			foreach (string s in jobs) {
				if (i >= limit)
					break;
				//Console.Clear ();
				Console.Write ("Converting job " + i++ + " of " + jobs.Count + Environment.NewLine);
				var name = Path.GetFileName(s);
				string id = System.Text.RegularExpressions.Regex.Replace (name, "\\..*", "");
				Job j = new Job ("test");
				if(fileType.ToLower() == "html")
					jobList.Add (j = Job.fromHTML(id));
				if(fileType.ToLower() == "json")
					jobList.Add (Job.fromJSON(id));
			}
			return jobList;
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
		public static void StartGUI (){
			Application.Init ();
			Window myWin = new Window ("Jobulator");
			myWin.Resize (300, 500);

			Button b;
			var vBox = new VBox ();
			/*
			foreach (Job j in jobs){
				b = new Button ();
				b.Label = j.Get ("id");
				vBox.Add (b);
			}
			*/
			myWin.Add (vBox);
			myWin.ShowAll();

			Application.Run();
		}
	}
}

