function like(id_post) { 
    const likeCount = document.getElementById(`likes-count-${id_post}`);
    const likeButton = document.getElementById(`like-button-${id_post}`);
    fetch(`/forum/like/${id_post}`, { method: "POST" }).then((res) => res.json()).then((data) => { 
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true) {
        likeButton.className = "fas fa-thumbs-up";
        } else {
        likeButton.className = "far fa-thumbs-up";
        }
    })
    .catch((e) => alert("Could not like post."));
}
