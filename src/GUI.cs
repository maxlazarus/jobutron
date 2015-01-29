using System;
using Gtk;

namespace jobulator {
	public class GUI {

		VBox vBox;
		Window window;

		public GUI (string s) {
			window = new Window (s);
			vBox = new VBox ();
		}

		public void Start (){
			Application.Init ();

			window.Resize (300, 500);
			window.DeleteEvent += OnDeleteEvent;
			AddButton ("Started");
			AddButton ("Yes");
			window.Add (vBox);
			window.ShowAll();

			Application.Run();
		}
		public void AddButton(string s) {
			Button b = new Button (s);
			b.Clicked += new EventHandler(ButtonPressHandler);
			vBox.Add (b);
			window.ShowAll ();
		}
		private void ButtonPressHandler(object o, EventArgs ea) {
			AddButton (o.ToString());
		}
		public void ListJobs(System.Collections.Generic.IEnumerable<Job> jobs) {
			foreach (Job j in jobs){
				var b = new Button ();
				b.Label = j.Get ("id");
				vBox.Add (b);
			}
		}
		static void OnDeleteEvent(object o, EventArgs ea) {
			Application.Quit ();
		}
	}
}

