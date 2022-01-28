import re
from scrapy.spiders import SitemapSpider
from ..items import XmRunItem

class XmSitemapSpider(SitemapSpider):
	name = 'xm_sitemap'
	allowed_domains = ['xmovies8.one']
	sitemap_urls = ['https://xmovies8.one/sitemap.xml']
	sitemap_rules = [('/movie/','parse_movie'), ('/tv/','parse_movie')]

	def parse(self, response):
		pass

	def parse_movie(self,response):
		item = XmRunItem()
		item['url'] = response.url
		item['x_id'] = response.selector.css("#main-wrapper").xpath("@data-id").get()
		item['tmdb_id'] = response.selector.css("div#watch-iframe").xpath("@data-tmdb-id").get()
		item['movie_url'] = response.selector.css("div#watch-iframe iframe").xpath("@src").get()
		base = response.selector.css("div.detail_page.watch_page img.film-poster-img")
		item['image_urls'] = [base.xpath("@src").get()]
		item['name'] = base.xpath("@title").get() or base.xpath("@alt")
		item['description'] = response.selector.css("div.detail_page.watch_page div.description::text").get().strip()
		item['vtype'] = re.search("/(tv|movie)/",item['url'],re.I)[1]
		_extra = response.css('div.detail_page.watch_page div.elements div.row-line')
		for line in _extra:
			_tmp  = "".join((k.get().strip() for k in line.xpath(".//text()"))).split(":")
			if(re.match("released",_tmp[0],re.I)):
				item['year'] = re.match(r"(\d{4})-.*",_tmp[1])[1]
			elif(re.match("duration",_tmp[0],re.I)):
				item['duration'] = _tmp[1]
			elif(re.match("genre",_tmp[0],re.I)):
				item['genre'] = _tmp[1].split(',')
			elif(re.match("country",_tmp[0],re.I)):
				item['country'] = _tmp[1].split(',')
		children = response.selector.css('div.film_related.file_realted-list div.flw-item')
		similar = []
		for child in children:
			_child_prop = {}
			_atag = child.css("div.film-poster a")
			_child_prop['url'] = response.urljoin(_atag.xpath('@href').get())
			_child_prop['name'] = _atag.xpath("@title").get()
			_child_prop['image_urls'] = [child.css("img").xpath("@data-src").get()]
			_child_prop['x_id'] = _atag.xpath("@data-id").get()
			_child_prop['vtype'] = re.search("/(tv|movie)/",_child_prop['url'],re.I)[1]
			if(re.search("/movie/",_child_prop['url'])):
				_child_prop['year'] = child.css("div.film-detail span.fdi-item::text").get()
				_child_prop['duration'] = child.css("div.film-detail span.fdi-item.fdi-duration::text").get()
			similar.append(_child_prop)
		item['similar'] = similar
		yield item

