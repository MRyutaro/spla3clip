import { Box } from "@mui/material";


export default function Footer(): JSX.Element {
    return (
        <Box
            sx={{
                bgcolor: "#4f2ede",
                color: "white",
                padding: 1,
                textAlign: "center",
            }}
        >
            <p>
                © 2024 MRyutaro, ItinoseGuren
            </p>
        </Box>
    );
}
