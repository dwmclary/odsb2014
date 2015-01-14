name := "NewsStreamer"
version := "0.1"
scalaVersion := "2.10.4"
libraryDependencies ++= Seq(
"org.apache.spark" %% "spark-core" % "1.1.0" % "provided", 
"org.apache.spark" %% "spark-streaming" % "1.1.0" % "provided",
"org.apache.spark" % "spark-streaming-flume_2.10" % "1.1.0" ,
"org.apache.hadoop" % "hadoop-client" % "2.3.0-cdh5.1.2",
"org.json4s" %% "json4s-jackson" % "3.2.11",
"org.json4s" %% "json4s-native" % "3.2.11").map({dep =>
dep.exclude("org.mortbay.jetty", "servlet-api").
        exclude("commons-beanutils", "commons-beanutils-core").
        exclude("commons-collections", "commons-collections").
        exclude("commons-collections", "commons-collections").
	exclude("commons-logging", "commons-logging").
        exclude("com.esotericsoftware.minlog", "minlog").
        exclude("asm", "asm").			     
        exclude("org.apache.hadoop", "hadoop-yarn-common")
})
resolvers += "Akka Repository" at "http://repo.akka.io/releases/"
resolvers += "Cloudera Repository" at "https://repository.cloudera.com/artifactory/cloudera-repos/"

mainClass in assembly := Some("com.oracle.newsstream.NewsStreamer")

mergeStrategy in assembly <<= (mergeStrategy in assembly) { (old) =>
  {
    case x if x.startsWith("META-INF/ECLIPSEF.RSA") => MergeStrategy.last
    case x if x.startsWith("META-INF/mailcap") => MergeStrategy.last
    case x if x.startsWith("META-INF/mimetypes") => MergeStrategy.last
    case x if x.startsWith("plugin.properties") => MergeStrategy.last
    case x if x.startsWith("javax") => MergeStrategy.first
    case x => old(x)
  }
}