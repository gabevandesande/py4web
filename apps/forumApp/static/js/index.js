// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        posts: [],
        user_email: user_email,
        author: author,
        result: [],
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
            p.server_content = p.content; // Content on the server.
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
        // Handler for button that starts the edit.
        // TODO: make sure that no OTHER post is being edited.
        // If so, do nothing.  Otherwise, proceed as below.
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
        }
    }

    app.do_save = (post_idx) => {
        // Handler for "Save edit" button.
        let p = app.vue.posts[post_idx];
        if (p.content !== p.server_content) {
            p.is_pending = true;
            axios.post(posts_url, {
                content: p.content,
                id: p.id,
                is_reply: p.is_reply,
                author: p.author,
            }).then((result) => {
                console.log("Received:", result.data);
                p.edit = false;
                p.original_content = p.content;
                p.server_content = result.data.content;
                p.is_pending = false;
                p.editable = true;
                p.author = app.data.author
                // TODO: You are receiving the post id (in case it was inserted),
                // and the content.  You need to set both, and to say that
                // the editing has terminated. DONE?
            }).catch(() => {
                p.is_pending = false;
                console.log("Caught error");
                // We stay in edit mode.
            });
        } else {
            // No need to save.
            p.edit = false;
            p.original_content = p.content;
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
            server_content: null,
            original_content: "",
            author: app.data.author,
            email: null,
            is_reply: null,
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
              server_content: null,
              original_content: "",
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
