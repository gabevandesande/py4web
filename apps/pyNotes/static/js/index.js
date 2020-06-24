let app = {};

let init = (app) => {

    // This is the Vue data.
    app.data = {
        posts: [],
        user_email: user_email,
        author: author,
        result: [],
        current_time: current_time,
    };

    app.index = (a) => {
        // Adds to the posts all the fields on which the UI relies.
        let i = 0;
        for (let p of a) {
            p._idx = i++;
            // TODO: Only make the user's own posts editable.
            p.editable = (p.email == app.data.user_email)
            p.edit = false;
            p.is_pending = false;
            p.error = false;
            p.original_content = p.content; // Content before an edit.
            p.server_content = p.content;
            p.original_title = p.title;
            p.server_title = p.title // Content on the server.
        }
        return a;
    };

    app.reindex = () => {
        // Adds to the posts all the fields on which the UI relies.
        let i = 0;
        for (let p of app.vue.posts) {
            p._idx = i++;
        }
    };

    app.do_edit = (post_idx) => {
        let p = app.vue.posts[post_idx];
        p.edit = true;
        p.is_pending = false;
    };

    app.do_cancel = (post_idx) => {
        // Handler for button that cancels the edit.
        let p = app.vue.posts[post_idx];
        if (p.id === null) {
            // If the post has not been saved yet, we delete it.
            app.vue.posts.splice(post_idx, 1);
            app.reindex();
        } else {
            // We go back to before the edit.
            p.edit = false;
            p.is_pending = false;
            p.content = p.original_content;
            p.title = p.original_title;
        }
    }

    app.do_save = (post_idx, color, starred) => {
        let p = app.vue.posts[post_idx];
        if ((p.content !== p.server_content) || (p.color !== color) || (p.title !== p.server_title) || (p.starred !== starred)) {
            p.is_pending = true;
            axios.post(posts_url, {
                content: p.content,
                id: p.id,
                is_reply: p.is_reply,
                author: p.author,
                color:color,
                title:p.title,
                starred:starred,
                post_date: app.data.current_time,
            }).then((result) => {
                console.log("Received:", result.data);
                p.edit = false;
                p.original_content = p.content;
                p.server_content = result.data.content;
                p.original_title = p.title;
                p.server_title = result.data.title;
                p.is_pending = false;
                p.editable = true;
                p.author = app.data.author;
                p.color = result.data.color;
                p.starred = result.data.starred;
                p.title = result.data.title;
                p.post_date = result.data.post_date
                // TODO: You are receiving the post id (in case it was inserted),
                // and the content.  You need to set both, and to say that
                // the editing has terminated. DONE?
            }).catch(() => {
                p.is_pending = false;
                console.log("Caught error");
                // We stay in edit mode.
            });
            axios.get(posts_url).then((result) => {
                let posts = result.data.posts;
                app.reindex(posts);
                app.vue.posts=app.index(posts);
            })
        } else {
            // No need to save.
            p.edit = false;
            p.original_content = p.content;
            p.original_title = p.title;
        }
    }

    app.add_post = () => {
        // TODO: this is the new post we are inserting.
        // You need to initialize it properly, completing below, and ...
        let q = {
            id: null,
            edit: true,
            editable: true,
            content: "",
            title: "",
            server_content: null,
            server_title:null,
            original_content: "",
            original_title: "",
            author: app.data.author,
            email: null,
            is_reply: null,
            color:"has-background-red",
            starred:false,
        };
        app.vue.posts.unshift(q)
        app.reindex();
    };

    app.reply = (post_idx) => {
        let p = app.vue.posts[post_idx];
        if (p.id !== null) {
            // TODO: this is the new reply.  You need to initialize it properly...
            let q = {
              id: null,
              edit: true,
              editable: app.data.editable,
              content: "",
              title: "",
              server_content: null,
              server_title:null,
              original_content: "",
              original_title:"",
              author: app.data.author,
              email: null,
              is_reply: p.id,
            };
            app.vue.posts.splice(p._idx + 1, 0, q)
            app.reindex();
            // DONE? TODO: and you need to insert it in the right place, and reindex
            // the posts.  Look at the code for app.add_post; it is similar.
        }
    };

    app.do_delete = (post_idx) => {
        let p = app.vue.posts[post_idx];
        if (p.id === null) {
          app.vue.posts.splice(post_idx, 1);
          app.reindex();
        } else {
          axios.post(delete_url, {id:p.id})
          app.vue.posts.splice(post_idx, 1);
          app.reindex();
        }
    };

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        do_edit: app.do_edit,
        do_cancel: app.do_cancel,
        do_save: app.do_save,
        add_post: app.add_post,
        reply: app.reply,
        do_delete: app.do_delete,
        reindex:app.reindex,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        axios.get(posts_url).then((result) => {
            let posts = result.data.posts;
            app.reindex(posts);
            app.vue.posts=app.index(posts);
        })
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
