using System;
using System.IO;
using System.Text.RegularExpressions;

namespace jobulator {
	public class FileHandler {

        public readonly static string
            slash = "",
            resPath = "",
            basePath = "",
            srcPath = "",
            binPath = "",
            osName = "";

		static FileHandler (){
			var os = System.Environment.OSVersion;
            osName = (os.ToString().Contains("Windows"))? "windows": "linux";
            slash = (osName == "windows")? "\\" : "/";
			basePath = ".." + slash + ".." + slash;
			resPath = basePath + "res" + slash;
			srcPath = basePath + "src" + slash;
            binPath = basePath + "bin" + slash + osName + slash;  
		}
		public static StreamReader Open (String s) {
			try {
				return new StreamReader(findPath(s));
			} catch {
				return null;
			}
		}
		public static string OpenAsString (String s) {
			StreamReader sr = new StreamReader(findPath(s));
			string line = "", document = "";
			while ((line = sr.ReadLine ()) != null) {
				document += line;
			}
			sr.Close ();
			return document;
		}
		public static void Write (string s, string name) {
			using (StreamWriter writer =
				new StreamWriter(resPath + name)) {
				writer.Write(s);
			}
		}
		public static System.Collections.Generic.List<string> getFileNames(string extension) {
			var dir = (extension.Contains ("html")) ? "jobs" + slash : "res" + slash;
			var filePaths = Directory.EnumerateFiles (basePath + dir, "*." + extension);
			return new System.Collections.Generic.List<string>(filePaths);
		}
		public static string findPath(string s) {
			var dir = "";
			dir = (s.Contains("html"))? "jobs" + slash: "res" + slash;
			dir = (s.Contains("cover"))? "covers" + slash: dir;
			return basePath + dir + s;
		}
	}
}


