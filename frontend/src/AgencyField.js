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
        axios.get(':8000/get_agencies/')
            .then(response => setUzaList(response.data));
    }, []);

    React.useEffect((event) => {
        props.setAgencyIds(filters)
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
                getOptionLabel={(option) => option.agency_name}
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
                    style={{width: "50%", alignContent: "center", alignItems: "center"}} 
                        {...params}
                        label="Filter by Transit Agencies"
                    />
                )}
            />
        )}  </div>
        //   <h1>{lastName}</h1>
    );
}