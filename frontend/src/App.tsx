import React, {useEffect, useState} from 'react';
import axios from "axios";
import {ICarModel} from "./interfaces/ICarModel";

const App = () => {

    const [cars, setCars] = useState<ICarModel[]>([])
    useEffect(() => {
        axios.get('/api/cars').then(({data})=>setCars(data.data))
    }, []);
    return (
        <div>
            <h1>Cars</h1>
            {cars.map(car=><div key={car.id}>{car.id} {car.model.name}</div>)}
        </div>
    );
};

export default App;