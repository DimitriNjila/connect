import React, { useEffect, useState } from "react";
import AddFruitForm from "./AddFruitForm";
import api from "../api";

interface Fruit {
  id: string;
  name: string;
  color: string;
}

const FruitList = () => {
  const [fruits, setFruits] = useState([]);

  const fetchFruits = async () => {
    try {
      const response = await api.get("/fruits");
      setFruits(response.data.fruits);
    } catch (error) {
      console.error("Error fetching fruits", error);
    }
  };

  const addFruit = async ({ name, color }) => {
    try {
      await api.post("/fruits", { name, color });
      fetchFruits(); // Refresh the list after adding a fruit
    } catch (error) {
      console.error("Error adding fruit", error);
    }
  };

  const deleteFruit = async (id: string) => {
    try {
      await api.delete(`/fruits/${id}`);
      fetchFruits(); // Refresh the list after deleting a fruit
    } catch (error) {
      console.error("Error deleting fruit", error);
    }
  };

  useEffect(() => {
    fetchFruits();
  }, []);

  return (
    <div>
      <h2>Fruits List</h2>
      <ul>
        {fruits.map((fruit) => (
          <li key={fruit.id}>
            {fruit.name}, {fruit.color}
            <button
              className="text-red-600 hover:underline"
              onClick={() => deleteFruit(fruit.id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
      <AddFruitForm addFruit={addFruit} />
    </div>
  );
};

export default FruitList;
