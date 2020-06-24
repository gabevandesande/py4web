(function(){

    var thumbrater = {
        props: ['url', 'callback_url'],
        data: null,
        methods: {}
    };

    thumbrater.data = function() {
        var data = {
            rating_display: 0,
            rating_assigned: 0,
            thumb_indices: [1,2],
            get_url: this.url,
            set_url: this.callback_url,
        };
        thumbrater.methods.load.call(data);
        return data;
    };

    thumbrater.methods.thumbs_over = function (thumb_idx) {
        // When hovering over a thumb, we display that many thumbs.
        console.log("Over:", thumb_idx);
        let self = this;
        self.rating_display = thumb_idx;
    };

    thumbrater.methods.thumbs_out = function () {
        // Sets the number of thumbs back to the number of true thumbs.
        let self = this;
        self.rating_display = self.rating_assigned;
    };

    thumbrater.methods.set_rating = function (thumb_idx) {
        // Sets and sends to the server the number of thumbs.
        let self = this;
        if(self.rating_assigned == thumb_idx){
          self.rating_assigned = 0;
        }
        else{
          self.rating_assigned = thumb_idx;
        }
        axios.get(self.set_url,
            {params: {rating: self.rating_assigned}});
    };

    thumbrater.methods.load = function () {
        // In use, self will correspond to the data of the table,
        // as this is called via grid.methods.load
        let self = this;
        axios.get(self.get_url)
            .then(function(res) {
                self.rating_assigned = res.data.rating;
                self.rating_display = res.data.rating;
            })
    };

    utils.register_vue_component('thumbrater', 'components/thumbrater/thumbrater.html',
        function(template) {
            thumbrater.template = template.data;
            return thumbrater;
        });
})();
