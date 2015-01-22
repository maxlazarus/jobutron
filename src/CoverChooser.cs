namespace jobulator {
	public class CoverChooser {
		public CoverChooser () {
		}
		public static string Choose( Job j ) {
			if (
				j.CategoryContains ("job_title", "software") |
				j.CategoryContains ("job_title", "developer") |
				j.CategoryContains ("industry", "software")) { 
				return "software.cover";
			} else {
				return "basic.cover";
			}
		}
	}
}

