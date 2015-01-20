using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;

namespace jobulator {
	
	class Regexer {
		delegate void del(string a, string b);

		public static string Convert(string text) {
			Regex regex = new Regex("(<.*?>\\s*)+", RegexOptions.Singleline);
			text = regex.Replace(text, "").Trim();

			string expiry = Regex.Match(text, @"Application Deadline:.*?Application Method").Groups[0].Value;
			expiry = Regex.Replace (expiry, @"Application Deadline:", @"");
			expiry = Regex.Replace (expiry, @"Application Method", @"");
			expiry = Regex.Replace (expiry, @"[\n\t\:]", "");

			string resultText = "application_deadline: " + expiry;
			regex = new Regex("Position Type.*");
			resultText += Environment.NewLine + regex.Match (text).Groups [0].Value;
			string newLine = Environment.NewLine;

			del reg = (x, y) => resultText = Regex.Replace (resultText, x, y, RegexOptions.Singleline);
			reg ('"' + "", "");
			reg (@"\s\s+", newLine);
			reg ("[\\n\\r]+2015[\\n\\r]+UBC.*", "");
			//reg ("Job Description:", "");
			reg ("Job Requirements:", newLine + "Job Requirements:");
			reg ("Position Description:", newLine + "Position Description:");
			reg (@"APPLICATION INFORMATION\s+", "");
			reg (@"ORGANIZATION INFORMATION\s+", "");
			reg (@"\s\(\$\)", "");
			reg (@"Work Term", "Workterm");
			reg ("©", "");
			reg (@"&amp;", @"&");

			return resultText;
		}
		public static KeyValuePair<string, string> ExtractKeyValuePair(string line) {
			line = Regex.Replace (line, '"' + "", "");
			var categoryTitle = Regex.Replace (line, ":.*", "");
			var data = "";
			try {
				data = Regex.Replace (line, categoryTitle + ":\\s?", "");
			} catch {
				Console.WriteLine ("regex error");
			}
			categoryTitle = Regex.Replace (categoryTitle, "[\\n\\r]+", "");
			categoryTitle = Regex.Replace (categoryTitle, "[\\s]+", "_");
			categoryTitle = categoryTitle.ToLower ();
			data = Regex.Replace (data, "[\\n\\r]+", "");
			return new KeyValuePair<string, string> (categoryTitle, data);
		}
	}
}
