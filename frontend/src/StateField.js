import * as React from 'react';
import Chip from '@mui/material/Chip';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import axios from "axios"
import Stack from '@mui/material/Stack';

export default function UzaField(props) {



    // const skillsOptions = skills.map(
    //     (skill, index) => (
    //         { 
    //             id: index + 1, 
    //             label: skill, 
    //         }
    //     )
    // )


    const [uzaList, setUzaList] = React.useState(null)
    const [filters, setFilters] = React.useState(null)
    // const [uzaIds, setUzaIds] = React.useState

    React.useEffect(() => {
        console.log(filters)
        axios.get('http://localhost:8000/get_states/')
            .then(response => setUzaList(response.data));
    }, []);

    React.useEffect((event) => {
        props.setStateIds(filters)
        console.log(filters)
    }, [filters])



    // const handleLastName = (event) => {
    //     setLastName(event.target.value);
    // };

    return (
        <div>  {uzaList && (
            <Autocomplete
                multiple
                id="tags-outlined"
                options={uzaList}
                getOptionLabel={(option) => option.state}
                // defaultValue={[uzaList[13]]}
                filterSelectedOptions
                onChange={(event, newValue) => {
                    setFilters(newValue)
                    // console.log(filters)
                    console.log(newValue)
                } 
                }
                renderInput={(params) => (
                    <TextField
                        {...params}
                        label="States"
                    />
                )}
            />
        )}  </div>
        //   <h1>{lastName}</h1>
    );
}