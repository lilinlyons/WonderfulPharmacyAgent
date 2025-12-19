import { useState, useEffect } from "react";
import { api } from "../components/utils/api";

export function useUsers() {
  const [users, setUsers] = useState([]);
  const [activeUser, setActiveUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .fetchUsers()
      .then((data) => {
        if (Array.isArray(data) && data.length) {
          setUsers(data);
          setActiveUser(data[0]);
        }
      })
      .finally(() => setLoading(false));
  }, []);

  return { users, activeUser, setActiveUser, loading };
}