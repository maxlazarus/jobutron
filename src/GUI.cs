using System;
using Gtk;
using Pango;

namespace jobulator {
	public class GUI {

		Window window;
		VBox vBox = new VBox ();
		HBox hBox = new HBox ();
		TextView textView = new TextView();

		public GUI (string s) {
			window = new Window (s);
			textView.WrapMode = Gtk.WrapMode.Word;
		}

		public void Start (){
			Application.Init ();

			window.Resize (800, 500);
			window.DeleteEvent += OnDeleteEvent;

			AddButton ("MORE BUTTONS!", (x, y) => AddButton("CHILD", (a, b) => {}));
			AddButton ("JOBS", (x, y) => ListJobs (Job.getJobsFrom("html", 5))); 

			hBox.Add (vBox);
			hBox.Add (textView);
			window.Add (hBox);
			window.ShowAll();

			Application.Run();
		}
		public void AddButton(string s, EventHandler e) {
			Button b = new Button (s);
			b.Clicked += e;
			vBox.Add (b);
			window.ShowAll ();
		}
		public void ListJobs(System.Collections.Generic.IEnumerable<Job> jobs) {
			foreach (Job j in jobs){
				AddButton (j.Get("id"), (x, y) 
					=> {
						textView.Buffer.Clear();
						textView.Buffer.InsertAtCursor(j.ToString());
					}
				);
			}
		}
		static void OnDeleteEvent(object o, EventArgs ea) {
			Application.Quit ();
		}
	}
}