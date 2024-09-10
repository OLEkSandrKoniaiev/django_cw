import React, {useEffect, useState} from 'react';
import axios from "axios";
import {CarModel} from "./interfaces/ICarModel";

const App = () => {

    const [cars, setCars] = useState<CarModel[]>([])
    useEffect(() => {
        axios.get('/api/cars').then(({data})=>setCars(data.data))
    }, []);
    return (
        <div>
            {cars.map(car=><div key={car.id}>{car.id} {car.brand}</div>)}
        </div>
    );
};

export default App;