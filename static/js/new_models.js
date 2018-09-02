function models(){
    window.Deneme = new Backbone.Collection;
    Deneme.url = '/crns';

    CrnList = Backbone.Collection;


window.Ders = Backbone.Model.extend({

  initialize: function() {
    this.cached ==false ;  //cache
    this.crnler = new CrnList;
    this.crnler.url = '/api/courses/' + this.id + '/sections';

//    this.crnler.bind("reset", this.updateCounts);
  },

  apiDersNo: function(ders_id) {

  this.crnler.url = '/api/courses/' + ders_id + '/sections';

  }

});


window.DersList = Backbone.Collection.extend({
  model: Ders
});


window.Bolum = Backbone.Model.extend({
  initialize: function() {
    _.bindAll(this, 'apiBolumNo' ,'cacheReady' );

    this.cached == false ;  //cache
    this.dersler = new DersList ;
    this.dersler.url = '/api/programs/' + this.id + '/courses';
  },

  apiBolumNo: function(bolum_id) {

  this.dersler.url = '/api/programs/' + bolum_id + '/courses';

  },

  cacheReady:function(){   //cache
      if (this.cached != true) {
          self=this; //SELF=THIS guzel mantik
                this.dersler.fetch({success: function(){self.cached=true; }  });
      }
  }
});


window.BolumList = Backbone.Collection.extend({
  model: Bolum
});
}
