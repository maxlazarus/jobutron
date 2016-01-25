namespace jobulator 
{
	public class CoverChooser 
    {
		public CoverChooser () 
        {
		}

		public static string Choose( Job j ) 
        {
            if (j.CategoryContains("job_title", "embedded")
                    | j.CategoryContains("job_description", "embedded"))
            {
                return "embedded.cover";
            }
            else if (j.CategoryContains("job_title", "robot"))
            {
                return "robotics.cover";
            } 
            else if(j.CategoryContains("job_title", "software") 
                    | j.CategoryContains("job_title", "developer")
				    | j.CategoryContains("industry", "software")) 
            { 
				return "software.cover";
            }

            return "basic.cover";
		}
	}
}

