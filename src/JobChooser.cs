namespace jobulator {
    class JobChooser {
        public static bool Test(Job j) {
            if ((
                j.CategoryContains("job_location", "vancouver") |
                j.CategoryContains("job_location", "burnaby") |
                j.CategoryContains("job_location", "richmond")
                ) && (
                j.CategoryContains("application_deadline", @"jan 22") &&
                !j.CategoryContains("job_title", "instructor")
            )){
                return true;
            }
            return false;
        }
    }
}
