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


//TEST
//var ders = new Ders();
//ders.apiDersNo(2);
//ders.crnler.fetch({success: function(){    console.log( ders ) ;   } , add: true });




window.DersList = Backbone.Collection.extend({
  model: Ders
});

window.Bolum = Backbone.Model.extend({

  initialize: function() {
    _.bindAll(this, 'apiBolumNo' ,'cacheReady' );

    this.cached == false ;  //cache
    this.dersler = new DersList ;
    this.dersler.url = '/api/programs/' + this.id + '/courses';

//    this.crnler.bind("reset", this.updateCounts);
  },

  apiBolumNo: function(bolum_id) {

  this.dersler.url = '/api/programs/' + bolum_id + '/courses';

  },

  cacheReady:function(){   //cache
      console.log("ready?");
      if (this.cached != true) {
          self=this; //SELF=THIS guzel mantik
                this.dersler.fetch({success: function(){    console.log("cached!") ;  self.cached=true; }  });

      }

  }

});



//TEST
//bolum = new Bolum;
//bolum.apiBolumNo(5);
//bolum.dersler.fetch({success: function(){    console.log( bolum ) ;   } , add: true });




window.BolumList = Backbone.Collection.extend({
  model: Bolum
});











}
