using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using Novacode;

namespace jobulator {
	
	public class CoverLetter {

		Job job;
		string n = Environment.NewLine;
		List<Paragraph> content = new List<Paragraph> ();

		public CoverLetter(Job j) 
        {
			job = j;
			string coverTemplate = "";
			coverTemplate = CoverChooser.Choose (j);

			StreamReader cl;

			try {
				cl = new StreamReader (FileHandler.findPath (coverTemplate));
			} catch {
				cl = new StreamReader (FileHandler.findPath ("example.cover"));
			}
			var p = new Paragraph ();
			string line = "";

			while ((line = cl.ReadLine ()) != null) {
				var matches = Regexer.Matches (line, @"(?<=\<)(.*?)(?=\>)");
				foreach (var v in matches)
					line = Regexer.Replace (line, @"<" + v + @">", j.Get (v));
				p.Add (line + n);
			}

			cl.Close ();
			content.Add (p);
		}

		public static void Generate(Job j) 
        {
			Console.WriteLine ("Generating cover letter for position " + j.Get ("id"));
			CoverLetter cl = new CoverLetter (j);
			cl.PrintDOCX ();
		}

		public void PrintDOCX() 
        {
			string fileName = FileHandler.resPath + job.Get("id") + @".docx";
			var doc = DocX.Create(fileName);
			foreach(Paragraph p in content)
				doc.InsertParagraph (p.ToString());
			try 
            {
				doc.Save();
			} 
            catch(Exception e) 
            {
				Console.WriteLine ("Document error in file(s) for " + job.Get("id"));
				Console.WriteLine (e.ToString ());
			}
			//System.Diagnostics.Process.Start("WINWORD.EXE", fileName);
		}
	}

	class Paragraph 
    {
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
