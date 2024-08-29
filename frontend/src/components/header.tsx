import { Box, Typography } from "@mui/material";


export default function Header(): JSX.Element {
    return (
        <Box
            sx={{
                bgcolor: "#4f2ede",
                color: "white",
                padding: 4,
            }}
        >
            <Typography variant="h4">
                Spla3Clip
            </Typography>
        </Box>
    );
}
