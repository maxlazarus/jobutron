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

		public CoverLetter(Job j) {
			job = j;
			Paragraph p = new Paragraph ();
			string preamble = "Maxim Prokopenko\n56 E 47th Avenue\nVancouver, BC\nCanada V5W 2A5\n\n" +
				"January 18, 2015\n\n\n" + job.Get ("company") + "\nc/o UBC Engineering Co-op office\n";
			p.Add (preamble);
			p.Add ("\nDear Sir or Madam:" + n);
			p.Add ("\nRe: Job # " + job.Get ("id") + " " + job.Get ("job_title") + "\n\n");

			p.Add ("This opportunity is an excellent match for my skills and I would be excited "+
				"to work as part of a multidisciplinary team.  My teamwork and communication skills "+
				"have been refined through years of varying experience in different work environments "+
				"and, combined with my technical skills, give me all the tools necessary to "+
				"make valuable contributions." + n + n);

			p.Add ("Attention to detail is a quality that is necessary for me as a 3rd year Electrical " +
				"Engineering student in the Nanotechnology Option at UBC.  Studying nanoscale systems " +
				"and quantum behaviour has taught me a respect for accuracy and analysis that will allow " +
				"me to independently develop solutions to problems." + n + n); 

			p.Add ("Being a part of the http://openrobotics.ca student team has increased my knowledge of " +
				"analog and digital circuits and given me experience using them in a practical setting.  By " +
				"applying this knowledge combined with my years of effectively communicating in challenging " +
				"construction and customer-facing environments I will be able to accurately perform tests and " +
				"measurements as well as co-ordinate with the other team members effectively." + n + n);

			p.Add ("This position has many interesting challenges and my skills " +
				"and proactive, enthusiastic attitude will allow me to assist " + job.Get("company") + " " +
				"in surmounting them. " +
				"I would be excited to learn about this industry and apply the knowledge I’ve gained at UBC "+
				"and working on group projects to this field. " +
				"Thank you for taking the time to consider me; " +
				"to arrange an interview, please contact the Co-op Office at 604-822-6995 or at " +
				"coop.interviews@ubc.ca." + n + n);

			p.Add (n + "Respectfully," + n + n);

			p.Add("-Maxim Prokopenko");
			content.Add (p);
		}

		public void printDOCX() {
			string fileName = FileHandler.resPath + job.Get("id") + @".docx";
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
