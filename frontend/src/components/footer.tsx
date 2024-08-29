import { Box } from "@mui/material";


export default function Footer(): JSX.Element {
    return (
        <Box
            sx={{
                bgcolor: "secondary.main",
                color: "white",
                padding: 1,
                textAlign: "center"
            }}
        >
            <p>
                © 2024 MRyutaro, ItinoseGuren
            </p>
        </Box>
    );
}
