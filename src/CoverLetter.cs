using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using Novacode;

namespace jobulator {
	
	public class CoverLetter {

		Job job;
		string test = "TESTS";
		List<Paragraph> content = new List<Paragraph> ();

		public CoverLetter(Job j) {
			job = j;
			Paragraph p = new Paragraph ();
			string preamble = "Maxim Prokopenko\n56 E 47th Avenue\nVancouver, BC\nCanada V5W 2A5\n\nJanuary 8, 2015\n\n\n" + job.Get ("company") + "\nc/o UBC Engineering Co-op office\n";
			p.Add (preamble);
			p.Add ("\nDear Sir or Madam:" + Environment.NewLine);
			p.Add ("\nRe: Job # " + job.Get ("id") + " " + job.Get ("job_title") + "\n\n");
			content.Add (p);

			Paragraph intro = new Paragraph ();
			p.Add ("");
		}

		public void printDOCX() {
			string fileName = FileHandler.resPath + test;
			var doc = DocX.Create(fileName);
			foreach(Paragraph p in content)
				doc.InsertParagraph (p.ToString());
			doc.Save();
			System.Diagnostics.Process.Start("WINWORD.EXE", fileName);
		}
	}
	class Paragraph {

		List<string> sentences = new List<string> ();

		public void Add(String s) {
			sentences.Add (s);
		}
		public override string ToString () {
			var output = "";
			foreach (string s in sentences)
				output += s;
			output += Environment.NewLine;
			return string.Format (output);
		}
	}
}
