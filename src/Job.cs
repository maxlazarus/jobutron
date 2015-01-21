using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace jobulator {
	public class Job {
		private Dictionary <string, Object> categories = new Dictionary <string, Object>();

		public Job (string id) {
			if(!Check(id))
				Add ("id", id);
		}

		public void Add(string s, Object o) {
			try {
				categories.Add (s, o);
			} catch {
				//Logger.log("Error adding " + a " of type " + o.ToString())
			}
		}
		public string Get(string s) {
			if (Check (s))
				return categories [s].ToString ();
			else
				return "";
		}
		public bool Check(string s) {
			return categories.ContainsKey (s);
		}
		public bool CategoryContains(string c, string s) {
			//CONVERTS TO LOWER CASE WHEN CHECKING
			if (Check (c)) {
				var lowerCase = categories [c].ToString ().ToLower ();
				return lowerCase.Contains (s);
			}
			return false;
		}
		public void Print() {
			foreach(KeyValuePair<string, Object> kvp in categories) {
				Console.WriteLine (kvp.Key + " : " + (string)kvp.Value);
			}
		}
		public void WriteJSON() {
			var s = "{";
			var comma = "";
			foreach(KeyValuePair<string, Object> kvp in categories) {
				s += comma;
				comma = ",";
				s += Environment.NewLine;
				s += "\t" + '"' + kvp.Key + '"' + " : " + '"' + (string)kvp.Value + '"';
			}
			s += Environment.NewLine + "}";
			FileHandler.Write (s, this.Get("id") + ".json");
		}
		public void Fill(string s) {
			foreach (var line in s.Split(new string[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries)) {
				KeyValuePair<string, string> kvp = Regexer.ExtractKeyValuePair (line);
				this.Add (kvp.Key, kvp.Value);
			}
		}
		public static Job fromHTML(string name) {
			string html = FileHandler.OpenAsString (name + @".html");
			var jText = Regexer.Convert (html);
			Job j = new Job (name);
			j.Fill (jText);
			return j;
		}
		public static Job fromJSON(string name) {
			System.IO.StreamReader f = FileHandler.Open (name + @".json");				
			if (f != null) {
				Job j = new Job (name);
				string line = "";

				while ((line = f.ReadLine ()) != null) {
					var m = Regex.Matches (line, "\\\"(.*?)\\\"");
					var e = m.GetEnumerator ();

					try {
						e.MoveNext ();
						var category = Regex.Replace(e.Current.ToString (), "\\\"", "");
						e.MoveNext ();
						var data = Regex.Replace(e.Current.ToString (), "\\\"", "");
						j.Add(category, data);
					} catch {
						//unreadable line
					}
				}
				f.Close ();
				return j;
			}
			return null;
		}
	}
}

