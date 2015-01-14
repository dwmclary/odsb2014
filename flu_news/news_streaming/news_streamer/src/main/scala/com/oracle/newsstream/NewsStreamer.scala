package com.oracle.newsstream

import org.json4s._
import org.json4s.jackson.Serialization.{read,write}
import org.apache.spark._
import org.apache.spark.rdd.RDD
import org.apache.spark.rdd._
import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._
import org.apache.spark.streaming.flume._
import scala.collection.immutable.StringOps


case class RSSItem(category : String, title : String, summary : String)


object NewsStreamer {
    def containsFlu(x : String): Boolean = x match {
      case x if x contains " flu " => true
      case x if x contains " influenza " => true
      case x if x contains " disease " => true
      case x if x contains " outbreak " => true
      case x if x contains " H1N1 " => true
      case x if x contains " H5N1 " => true
      case x if x contains " sick " => true
      case _ => false
    }

  def main(args : Array[String]) = {
    val conf = new SparkConf().setAppName("NewsStreamer")
    val ssc = new StreamingContext(conf, Seconds(30))
    
    val flumeStream = FlumeUtils.createStream(ssc, "localhost", 44444)
    val rssData = flumeStream.map(record => {
	implicit val formats = DefaultFormats
        read[RSSItem](new String(record.event.getBody().array()))
	})
    val healthSummaries = rssData.filter(x => containsFlu(x.summary))

    // print batch summaries to the screen
    rssData.count().map(cnt => "rss recv " + cnt + " events").print()

    val hsc = healthSummaries.count()
    hsc.map(cnt => "health summaries recv " + cnt + " events").print()
    
    //write health data out to HDFS
    val now: Long = System.currentTimeMillis
    healthSummaries.foreachRDD(r => {
	    if (r.count() > 0) {
              r.map(item => {
                implicit val formats = DefaultFormats
                write(item)
		  }).saveAsTextFile("/user/oracle/flu_streaming/flu_stream-"+now.toString())
		}
	})
    ssc.start()
    ssc.awaitTermination()
  }
}
