package com.oracle.newscluster

import org.json4s._
import org.json4s.jackson.Serialization.{read,write}
import org.apache.spark._
import org.apache.spark.SparkContext._
import org.apache.spark.rdd.RDD
import org.apache.spark.rdd._
import org.apache.spark.mllib.clustering.KMeans
import org.apache.spark.mllib.feature.Word2Vec
import org.apache.spark.mllib.feature.Word2VecModel
import org.apache.spark.mllib.linalg._

case class NewsArticle(date : String, title : String, byline : String, fulltext : String)

object NewsClustering {
  def sumArray (m: Array[Double], n: Array[Double]): Array[Double] = {
    for (i <- 0 until m.length) {m(i) += n(i)}
    return m
  }

  def divArray (m: Array[Double], divisor: Double) : Array[Double] = {
    for (i <- 0 until m.length) {m(i) /= divisor}
    return m
  }

  def wordToVector (w:String, m: Word2VecModel): Vector = {
    try {
      return m.transform(w)
    } catch {
      case e: Exception => return Vectors.zeros(100)
    }
  }
  
  def main(args : Array[String]) = {
    val sc = new SparkContext(new SparkConf().setAppName("News Clustering"))
    
    val news_rdd = sc.textFile("hdfs://localhost:8020/user/oracle/flu_news")

    val news_json = news_rdd.map(record => {
      implicit val formats = DefaultFormats
      read[NewsArticle](record)
    })

    val news_titles = news_json.map(_.title.split(" ").toSeq)
    val news_title_words = news_titles.flatMap(x => x).map(x => Seq(x))
    
    val w2v_input = sc.textFile("file:///home/oracle/odsb2014/flu_news/data/linewise_text_8").sample(false, 0.25,2).map(x => Seq(x))
    val all_input = w2v_input ++ news_title_words

    val word2vec = new Word2Vec()
    val model = word2vec.fit(all_input)

    val title_vectors = news_titles.map(x => new DenseVector(divArray(x.map(m => wordToVector(m, model).toArray).reduceLeft(sumArray),x.length)).asInstanceOf[Vector])     
    val title_pairs = news_titles.map(x => (x,new DenseVector(divArray(x.map(m => wordToVector(m, model).toArray).reduceLeft(sumArray),x.length)).asInstanceOf[Vector]))

    var numClusters = 100
    val numIterations = 25

    var clusters = KMeans.train(title_vectors, numClusters, numIterations)
    var wssse = clusters.computeCost(title_vectors)
    println("WSSSE for clusters:"+wssse)

    val article_membership = title_pairs.map(x => (clusters.predict(x._2), x._1))
    val cluster_centers = sc.parallelize(clusters.clusterCenters.zipWithIndex.map{ e => (e._2,e._1)})
    val cluster_topics = cluster_centers.mapValues(x => model.findSynonyms(x,5).map(x => x._1))

    var sample_topic = cluster_topics.take(12)
    var sample_members = article_membership.filter(x => x._1 == 6).take(10)
    for (i <- 6 until 12) {
	println("Topic Group #"+i)
	println(sample_topic(i)._2.mkString(","))
	println("-----------------------------")
	sample_members = article_membership.filter(x => x._1 == i).take(10)
	sample_members.foreach{x => println(x._2.mkString(" "))}
	println("-----------------------------")
    }

    article_membership.map{x => x._1.toString+","+x._2.mkString(" ")}.saveAsTextFile("/user/oracle/flu_news_categorization")
    cluster_topics.map{x => x._1+","+x._2.mkString(" ")}.saveAsTextFile("/user/oracle/flu_news_categories")

  }

}


