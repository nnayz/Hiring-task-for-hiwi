import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";


const ThreadList = () => {
    const [threads, setThreads] = useState([]);
    const navigate = useNavigate();
    const [newThread, setNewThread] = useState("");
    const [refetch, setRefetch] = useState(false);

    useEffect(() => {
        const fetchThreads = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/`);
                setThreads(response.data);
            } catch (error) {
                console.error("Error getting threads", error);
            }
        }

        fetchThreads();
    }, [refetch]);

    
    const handleViewThread = (id) => {
       navigate(`/view-thread/${id}`)
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`http://127.0.0.1:8000/thread`, { title: newThread });
            console.log(response);
            setThreads(prevThreads => [...prevThreads, { title: newThread, id: response.data.id }]);
            setRefetch((k) => !k);
            setNewThread("");
        } catch (error) {
            console.error("Error creating thread, ", error);
        }
    }

    const handleDelete = (id) => {
        const deleteThread = async () => {
            try {
                const response = await axios.delete(`http://127.0.0.1:8000/thread/${id}`);
                console.log(response);
            } catch (error) {
                console.error("Error deleting the thread, ", error);
            }
        }

        deleteThread();
        setThreads((prevThreads) => prevThreads.filter(thread => thread.id !== id));
    }

    return (
        <>
        <div className="thread-list">
            {threads.map((thread) => (
                
                <div key={thread.id} className="thread">{thread.title}
                <div>
                    <button className="btn" onClick={() => handleViewThread(thread.id)} style={{"marginRight": "10px"}}>View Thread</button>
                    <button className="delete-btn" onClick={() => handleDelete(thread.id)}>Delete Thread</button>
                </div>
                </div>

            ))}
            <form className="new-thread" onSubmit={handleSubmit}>
                <input 
                type="text"
                value={newThread}
                placeholder="Add New Thread ..."
                onChange={(e) => setNewThread(e.target.value)}
                />
                <button className="btn">Create</button>
            </form>
        </div>
        </>
    )
}

export default ThreadList;