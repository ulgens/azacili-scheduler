function views() {

    AppView = Backbone.View.extend({
        el: $("body"),
        initialize: function() {
            console.log("calistiii");

            //Create a friends collection when the view is initialized.
            //Pass it a reference to this view to create a connection between the two
        },
        events: {
            "click #save-program": "saveProgram"
        },
        saveProgram: function() {
            console.log("save?");
            button = $("#save-program");
            if (!button.hasClass('disabled')) {
                console.log("save!");
                $("#save-program").addClass("disabled");
                $("#save-program").removeClass("primary");
                $("#save-program").addClass("error");

                $("#save-program").html("Kaydediliyor...");

                $.ajax({
                    type: "POST",
                    url: "/save",
                    data: $("#save-program").attr("data")
                }).done(function(msg) {
                    //alert( "Data Saved: " + msg );
                    $("#save-program").html("Kaydedildi");
                    $("#save-program").removeClass("error");
                    $("#save-program").addClass("success");
                });
            }
            return false;
        }

    });

    window.appview = new AppView;

    //crn

    CrnView = Backbone.View.extend({
        tagName: "li",
        initialize: function() {
            console.log("CrnView: initialize");

            _.bindAll(this, 'render', 'selectCrn', 'renderDers', 'renderCrn', 'crnChanged');

            //this.render();
        },
        events: {
            "change #bolum": "renderDers",
            "change #ders": "renderCrn",
            "change #crn": "crnChanged",
            "click #crn-delete": "remove"
        },

        render: function() { //burada
            self = this;
            var template = _.template($("#crn-template").html(), {
                bolumler: bolumlist
            });
            // Load the compiled HTML into the Backbone "el"
            $(this.el).html(template);



            //selectDers("93", "1617", "20606-3367");

            //console.log("OOOOOOOOOOOOOOOO");




            return this; // arka().arkaya().fonk().yazmak icin  AMA return false gibi asil islevi engelliyor
        },



        selectCrn: function(bolum_id, ders_id, crn_val, callback) {
            self = this;

            function selectCrn(ders_id, crn_val) {
                if (bolumlist.get(bolum_id).dersler.get(ders_id).cached) {
                    self.renderCrn();
                    $("#crn", self.el).val(crn_val);
                    self.crnChanged();
                    if (typeof callback === 'function') {
                        callback();
                    }
                    //$(this.el).trigger('crn-changed', 'Hello World!');
                } else {
                    bolumlist.get(bolum_id).dersler.get(ders_id).crnler.fetch({
                        success: function() {
                            console.log("crnler cached for:" + ders_id);
                            bolumlist.get(bolum_id).dersler.get(ders_id).cached = true;
                            self.renderCrn();
                            $("#crn", self.el).val(crn_val);
                            self.crnChanged();
                            if (typeof callback === 'function') {
                                callback();
                            }
                            //        $(this.el).trigger('crn-changed', 'Hello World!');
                        }
                    });
                }
            }


            function selectDers(bolum_id, ders_id, crn_val) {
                console.log("AAAAA," + bolum_id + " * " + ders_id + " * " + crn_val)
                $("#bolum", self.el).val(bolum_id);


                if (bolumlist.get(bolum_id).cached) {
                    self.renderDers();
                    $("#ders", self.el).val(ders_id);
                    selectCrn(ders_id, crn_val);
                } else {
                    bolumlist.get(bolum_id).dersler.fetch({
                        success: function() {
                            console.log("dersler cached!");
                            bolumlist.get(bolum_id).cached = true;
                            self.renderDers();
                            $("#ders", self.el).val(ders_id);
                            selectCrn(ders_id, crn_val);
                        }
                    });
                }
            }

            selectDers(bolum_id, ders_id, crn_val);

        },


        renderDers: function() {
            self = this;


            bolum_id = $("#bolum", this.el).val();
            if (bolum_id != "-") {
                console.log("talimat?");
                if (bolumlist.get(bolum_id).cached) {
                    var template = _.template($("#ders-select").html(), {
                        dersler: bolumlist.get(bolum_id).dersler
                    }); // $("#ders", this.el).val()
                    $("#ders", self.el).html(template);
                    var template = _.template($("#crn-select").html(), {
                        crnler: "-"
                    });
                    $("#crn", self.el).html(template);
                } else {
                    bolumlist.get(bolum_id).dersler.fetch({
                        success: function() {
                            console.log("dersler cached!");
                            bolumlist.get(bolum_id).cached = true;
                            var template = _.template($("#ders-select").html(), {
                                dersler: bolumlist.get(bolum_id).dersler
                            })
                            $("#ders", self.el).html(template);
                            var template = _.template($("#crn-select").html(), {
                                crnler: "-"
                            });
                            $("#crn", self.el).html(template);
                        }
                    });
                }


            } else {
                var template = _.template($("#ders-select").html(), {
                    dersler: "-"
                });
                $("#ders", self.el).html(template);
                var template = _.template($("#crn-select").html(), {
                    crnler: "-"
                });
                $("#crn", self.el).html(template);
            }
            // Load the compiled HTML into the Backbone "el"
        },


        renderCrn: function() {
            self = this;

            bolum_id = $("#bolum", self.el).val();
            ders_id = $("#ders", self.el).val();

            if (ders_id != "-") {
                console.log("talimat?");
                if (bolumlist.get(bolum_id).dersler.get(ders_id).cached) {
                    var template = _.template($("#crn-select").html(), {
                        crnler: bolumlist.get(bolum_id).dersler.get(ders_id).crnler
                    }); // $("#ders", this.el).val()
                    $("#crn", self.el).html(template);
                } else {
                    bolumlist.get(bolum_id).dersler.get(ders_id).crnler.fetch({
                        success: function() {
                            console.log("crnler cached!");
                            bolumlist.get(bolum_id).dersler.get(ders_id).cached = true;
                            var template = _.template($("#crn-select").html(), {
                                crnler: bolumlist.get(bolum_id).dersler.get(ders_id).crnler
                            })
                            $("#crn", self.el).html(template);
                        }
                    });
                }

                //Yillar sonra edit, forum ekle
                var kod_fs = bolumlist.get(bolum_id).dersler.get(ders_id).get("kod");
                $("#forum-search", self.el).show().attr("href", "/forum?search=" + kod_fs);

            } else {
                var template = _.template($("#crn-select").html(), {
                    crnler: "-"
                });
                $("#crn", self.el).html(template);
            }
            // Load the compiled HTML into the Backbone "el"

        },


        crnChanged: function() {
            console.log("crn.change");
            // CrnListView.renderTable();
            $(this.el).trigger('crn-changed', 'Hello World!');
        },

        destroy: function() {
            this.model.destroy();
        },

        remove: function() {
            self = this
            $("#crn", self.el).val("-");
            $(self.el).trigger('crn-changed', 'Hello World!');
            $(self.el).remove();
            return false; //linkin calismamasi icin
        }
    });

    CrnListView = Backbone.View.extend({
        el: $("#crn-list"),
        initialize: function() {
            console.log("CrnListView: initialize");
            _.bindAll(this, 'render', 'renderTable', 'renderSaveButton');

            this.render();
            $(this.el).bind('crn-changed', this.renderTable);
            $(this.el).bind('crn-changed', this.renderSaveButton);
            $(this.el).bind('crn-changed', this.renderCrnEasyCopy);
        },
        events: {

            "click #crn-new": "addCrn"
        },

        render: function() {
            self = this;

            console.log("CrnListView: render");

            //            var view = new CrnView();
            //            console.log(view.el);
            //            view.el=$('.crn-row',this.el)

            $('li', self.el).each(function(index, element) {
                var view = new CrnView({
                    el: element
                });

                console.log(view.el);
            });

            self.renderTable();
            self.renderCrnEasyCopy();


        },

        addCrn: function() {
            console.log("CrnListView: addCrn");
            var view = new CrnView();

            view.render()
            $("ul", this.el).append(view.el);
            console.log(view.el);
            return false; //linkin calismamasi icin
        },
        addCrnWithCode: function() {
            console.log("CrnListView: addCrn");
            var view = new CrnView();

            view.render()
            $("ul", this.el).append(view.el);
            console.log(view.el);
            return view;
        },

        renderTable: function() {
            console.log("CrnListView:renderTable");
            var selected_crns = new Array;

            $('.crn-row', this.el).each(function(index) {
                bolum_id = $("#bolum", this).val();
                ders_id = $("#ders", this).val();
                crn_id = $("#crn", this).val();

                if (crn_id != "-") {
                    crn = bolumlist.get(bolum_id).dersler.get(ders_id).crnler.get(crn_id.split("/")[1]);

                    console.log(crn);
                    if (crn.get("bloklar")[0].saat1) {
                        selected_crns.push(crn);
                    }
                }
            });

            //console.log(crn_id.split("-")[0]);


            $("td").css('background', 'white');
            $("td:not(.saat)").html("");

            var saatler = new Array;


            selected_crns.forEach(function(crn, index, array) {

                crn.get("bloklar").forEach(function(blok, index, array) {
                    //console.log(blok);
                    saat1 = Number(blok.saat1.slice(0, 2));
                    saat2 = Number(blok.saat2.slice(0, 2));

                    while (saat1 < saat2) {
                        s = 'td[gun="' + blok.gun + '"][saat="' + saat1 + '"]';

                        saatler.push(blok.gun + "-" + saat1);

                        $(s).css('background', '#DBFF94');
                        $(s).html(crn.get("ders_adi"));
                        console.log(crn.get("ders_adi"));
                        //  console.log( saat1 );
                        saat1 = saat1 + 1;
                    }

                });
            });

            arr = saatler;
            var dup = [];

            for (var i = 0; i < arr.length; i++) {
                if (dup.indexOf(arr[i]) === -1 &&
                    arr.indexOf(arr[i], i + 1) !== -1) {
                    dup.push(arr[i]);
                }
            }

            dup.forEach(function(data, index, array) {
                console.log(data);
                s = 'td[gun="' + data.split("-")[0] + '"][saat="' + data.split("-")[1] + '"]';
                $(s).css('background', '#FF8566');

            });


            //$("td").css('background', 'white');

            //$(s).css('background', 'green');


        },

        renderSaveButton: function() {
            selected_crns = new Array;

            $('.crn-row', this.el).each(function(index) {
                crn_id = $("#crn", this).val();
                selected_crns.push(crn_id.split("/")[0]);
            });

            params = new Object;
            params.selected_crns = JSON.stringify(selected_crns);

            $("#save-program").addClass("primary");
            $("#save-program").html("Kaydet!");
            $("#save-program").removeClass("disabled");
            $("#save-program").removeClass("success");
            console.log(params);
            $("#save-program").attr("data", $.param(params));
        },

        renderCrnEasyCopy: function() {

            selected_crns = new Array;

            $('.crn-row', this.el).each(function(index) {
                var crn_id = $("#crn", this).val();
                var val = crn_id.split("/")[0];
                if (val != "-") {
                    selected_crns.push(val);
                }

            });




            s = ""
            //selected_crns.forEach(function(crn, index, array){            s=s+index+"="+crn+"&";   });

            for (var i = 0; i < selected_crns.length; i++) {
                crn = selected_crns[i];
                if (crn != "") {
                    s = s + ", " + crn;
                }
            }
            s = s.substr(1);

            $("#crn-easy-copy").html(s);


            //js kodu
            var jscode = 'javascript: (function(){ var crn=[' + selected_crns.join() + '];for(var i=0;i<crn.length;i++){var d=document.getElementById("crn_id"+(i+1));d.value=crn[i];}void(0);  })();';
            $("#crn-easy-fill").attr("href", jscode);

        }



    });



    window.crnlistview = new CrnListView;




}
