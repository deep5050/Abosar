const request = require('request');
const cheerio = require('cheerio');
const log = require('signale');
const fs = require('fs');

const options = {
    url: "https://www.anandabazar.com/supplementary/rabibashoriyo/a-short-story-wrinmukti-written-by-ujjwal-roy-1.1147478",
    headers: {
        'User-Agent': 'request'
    }
}

request.get(options,(error,response,html)=>{
    if(error)
    {
        log.error("could not fetch the source");
        
    }
    else if(!error && response.statusCode === 200)
    {
        
        
        log.success("successfully fetched");
        const $ = cheerio.load(html);
        
        var story_name = $('div[class="col-12 abp-storypage-headline"]').text().trim();
        var story_name_html = '<h1 align=center>'+story_name+'</h1>\n';



        var author = $('ul[class="author"]').text().trim();
        var author_html = '<h2 align=center>'+author+'</h2>\n';
       




        var img_div = $('div[id="abp-storypage-img-section"]');
        var img_src = img_div.find('img[class="img-fluid"]').attr('src'); // returns with leading '//'
        img_src = img_src.substr(2);
        img_html = '<div align=center> <img src="http://'+img_src +'" alt="'+ story_name + '" align="center" ></div>\n';
        



        var text = $("div[class='col-12 abp-storypage-articlebody abp-videoarticle-content']").html().trim();
       





        // create a write stream 
        out_stream = fs.createWriteStream('./stories/'+story_name+'.md');
       
        out_stream.write(img_html);
        out_stream.write(story_name_html);
        out_stream.write(author_html);
        out_stream.write(text);

        out_stream.destroy();
       
    }
});
