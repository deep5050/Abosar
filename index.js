const request = require('request');
const cheerio = require('cheerio');
const log = require('signale');
const fs = require('fs');
const {crawl_a_story} = require('./scraper/crawl');



if (!fs.existsSync('./stories')) {
    fs.mkdirSync('./stories');
}
if (!fs.existsSync('./stories/rabibasariya')) {
    fs.mkdirSync('./stories/rabibasariya');
}
if (!fs.existsSync('./metadata')) {
    fs.mkdirSync('./metadata');
}
if (!fs.existsSync('./metadata/rabibasariya')) {
    fs.mkdirSync('./metadata/rabibasariya');
}

if (!fs.existsSync('./metadata/images')) {
    fs.mkdirSync('./metadata/images');
}
if (!fs.existsSync('./metadata/images/rabibasariya')) {
    fs.mkdirSync('./metadata/images/rabibasariya');
}











//---------------------------------------------------------------


function get_recent_stories(url) {
    var options = {
        url: url,
        headers: {
            'User-Agent': 'request'
        }
    };

    request.get(options, (error, response, html) => {
        if (error) {
            log.error("could not fetch the source");
        }
        else if (!error && response.statusCode === 200) {
            const $ = cheerio.load(html);

            $('article[class="search-result row"]').each(function (index, elem) {
                var article_link = "https://www.anandabazar.com" + $(elem).find('a[class = "thumbnail"]').attr('href').trim();

                // now get only the links that contains the word 'short-story'
                if (article_link.search('short-story') !== -1) {

                    log.start(article_link);
                    crawl_a_story(article_link);

                }

            })
        }
    });
}

//---------------------------------------------------------------




const rabibashoriyo_url = "https://www.anandabazar.com/supplementary/rabibashoriyo/archive?page=1&slab=0&tnp=50";

get_recent_stories(rabibashoriyo_url);



