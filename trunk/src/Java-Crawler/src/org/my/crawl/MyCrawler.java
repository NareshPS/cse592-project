package org.my.crawl;


/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;
import java.util.regex.Pattern;

import org.apache.log4j.Logger;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import edu.uci.ics.crawler4j.crawler.Configurations;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.crawler.HTMLParser;
import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.PageFetchStatus;
import edu.uci.ics.crawler4j.crawler.PageFetcher;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.frontier.DocIDServer;
import edu.uci.ics.crawler4j.frontier.Frontier;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;
import edu.uci.ics.crawler4j.url.URLCanonicalizer;
import edu.uci.ics.crawler4j.url.WebURL;

/**
 * @author Yasser Ganjisaffar <yganjisa at uci dot edu>
 */

public class MyCrawler extends WebCrawler {
	
	FileWriter fstream ;
	BufferedWriter out ;
    int ID;
	public MyCrawler() throws IOException {
		// TODO Auto-generated constructor stub
		ID = 171;
		fstream = new FileWriter("C:/Users/nehal/workspace/Java-Crawler/DATA/" +this.ID+ ".txt");
		out = new BufferedWriter(fstream);
	}
	
	
	  Pattern filters = Pattern.compile(".*(\\.(css|js|bmp|gif|jpe?g"
            + "|png|tiff?|mid|mp2|mp3|mp4"
            + "|wav|avi|mov|mpeg|ram|m4v|pdf"
            + "|rm|smil|wmv|swf|wma|zip|rar|gz))$");

    /*
     * You should implement this function to specify
     * whether the given URL should be visited or not.
     */
	  // Questionable Content  
	  // Nukkes 94
	  // reallife 1278
	  // GPF 252
	  // crfh 343
	  // traingles and robot 171
	  // sheldon 613
    public boolean shouldVisit(WebURL url) {
            String href = url.getURL().toLowerCase();
            if (filters.matcher(href).matches()) {
                    return false;
            }
            if (href.startsWith("http://www.ohnorobot.com/archive.pl?comic="+this.ID+";show=2")) {
                    return true;
            }
            return false;
    }

    /*
     * This function is called when a page is fetched
     * and ready to be processed by your program
     */
    public void visit(Page page) {
            String empty = "";
    		int docid = page.getWebURL().getDocid();
            String url = page.getWebURL().getURL();         
            String HTML = page.getHTML();
            String text = page.getText();
            List<WebURL> links = page.getURLs();
            Document doc = Jsoup.parse(HTML); 
            Elements element = doc.select("table");
          //  System.out.print(element.text());
            Elements tds = element.select("td");
            if(element.text().isEmpty())
            return ;	
           
            for (Element td : tds) {
               Element slink = td.getElementsByClass("searchlink").first();
               if(slink == null){
            	   try {
            		   
            		  if(td.text().contains("untranscribed"))
            			   continue;
            	
            	   Element link = td.getElementsByClass("tinylink").first();
            		if(link == null){
            		continue;		
            		}
            		out.write(link.text());
            		out.newLine();
            		
            		//td.removeClass("tinylink");
            		 out.write(td.text());
 					  out.newLine();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
            	
               }
               else{
            	 /*  try {
            		   if(slink.text().contains("untranscribed"))
            			   continue;
					out.write(slink.text());
					out.newLine();
	            	   
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}*/
            	   
               }
            	   
            }          
           /* try {
            	out.write("Transcript: ");
				out.write(element.text());
				out.newLine();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}*/
    }
}