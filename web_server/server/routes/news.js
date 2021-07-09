var express = require('express');
var path = require('path');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res, next) {

    news = [
        {
            'url': 'https://edition.cnn.com/2021/07/08/us/young-victims-share-casket/index.html',
            'title': 'Two of the youngest victims of the Surfside collapse shared a casket, priest says',
            'description': 'Pallbearers carry the casket of two sisters killed in the Sunrise, Florida, condo collapse.',
            'source': 'cnn',
            'urlToImage': 'https://cdn.cnn.com/cnnnext/dam/assets/210708124959-guara-daughters-casket-0706-exlarge-169.jpg',
            'digest': '1',
            'reason': 'Recommend'
        },
        {
            'url': 'https://bleacherreport.com/articles/2945695-milwaukee-bucks-wasting-giannis-antetokounmpos-miracle-recovery?utm_source=cnn.com&utm_medium=referral&utm_campaign=editorial',
            'title': 'Milwaukee Bucks Wasting Giannis Antetokounmpo\'s Miracle Recovery',
            'description': 'After their 118-108 Game 2 victory over the Milwaukee Bucks, the Phoenix Suns are halfway to the first championship in franchise history.',
            'source': 'cnn',
            'urlToImage': 'https://media.bleacherreport.com/w_800,h_533,c_fill/br-img-images/003/915/243/hi-res-830abbdea79a9ec7c684574f33940504_crop_north.jpg',
            'digest': '2',
            'reason': 'Hot'
        }
    ]

    res.json(news);
});

module.exports = router;
