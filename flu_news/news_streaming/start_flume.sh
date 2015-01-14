#! /bin/bash
flume-ng agent --name newsAgent --conf-file ./flu_news_flume_config -f /usr/lib/flume-ng/conf/flume-conf.properties.template -Dflume.root.logger=DEBUG,console
