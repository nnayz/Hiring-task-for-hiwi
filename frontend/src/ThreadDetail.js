import axios from "axios";
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const ThreadDetail = () => {
    const navigate = useNavigate();
    const { threadId } = useParams();
    const [thread, setThread] = useState();
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState("");
    const [editedComment, setEditedComment] = useState("");
    const [editingId, setEditingId] = useState(null);

    useEffect(() => {
        const fetchThread = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/thread/${threadId}`);
                setThread(response.data);
            } catch (error) {
                console.error("Error fetching thread:  ", error);
            }
        }

        const fetchComments = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/thread/${threadId}/comments`);
                setComments(response.data);
            } catch (error) {
                console.error("Error fetching comments: ", error);
            }
        }

        fetchThread();
        fetchComments();
    }, [threadId]);

    const handleDeleteComment = (id) => {
        const deleteComment = async () => {
            try {
                const response = await axios.delete(`http://127.0.0.1:8000/comment/${id}`);
                console.log(response);
            } catch (error) {
                console.error("Error deleting comment", error);
            }
        }

        deleteComment();
        setComments((prevComments) => prevComments.filter(comment => comment.id !== id));
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`http://127.0.0.1:8000/thread/${threadId}/comments`, { content: newComment });
            console.log(response);
            setComments(prevComments => [...prevComments, response.data]);
            setNewComment("");
        } catch (error) {
            console.error("Error posting comment, ", error);
        }
    }

    const handleEditComment = async () => {
        if (editingId !== null) {
            try {
                const response = await axios.put(`http://127.0.0.1:8000/comment/${editingId}`, { content: editedComment });
                console.log(response);
                setComments((prevComments) => prevComments.map(comment => 
                    comment.id === editingId ? { ...comment, content: editedComment } : comment
                ));
                setEditingId(null); // Clear editing state
                setEditedComment(""); // Reset the edited comment field
            } catch (error) {
                console.error("Error editing comment", error);
            }
        }
    }

    // Start editing a comment
    const handleStartEditing = (comment) => {
        setEditingId(comment.id);
        setEditedComment(comment.content);
    }

    const handleBackButton = () => {
        navigate('/');
    }

    return (
        <div>
            <div>
                <button className="btn" onClick={handleBackButton}>&lt;</button>
                <h1>{thread ? thread.title : "Loading..."}</h1></div>
            {comments && comments.map((comment) => (
                <div key={comment.id} className="comment">
                    {editingId === comment.id ? (
                        <div style={{"display": "flex", "flexDirection": "column"}} className="edit-comment">
                            <textarea
                                type="text"
                                value={editedComment}
                                onChange={(e) => setEditedComment(e.target.value)}
                            />
                            <button className="btn" onClick={handleEditComment}>Save</button>
                        </div>
                    ) : (
                        <div>
                            <p>{comment.content}</p>
                            <button className="btn" onClick={() => handleStartEditing(comment)}>Edit Comment</button>
                        </div>
                    )}
                    <button className="delete-btn" onClick={() => handleDeleteComment(comment.id)}>&times;</button>
                </div>
            ))}
            <form className="new-comment" onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder="Add Comment ..."
                />
                <button className="btn">Post</button>
            </form>
        </div>
    )
}

export default ThreadDetail;