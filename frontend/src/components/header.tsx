import { Box } from "@mui/material";


export default function Header(): JSX.Element {
    return (
        <Box
            sx={{
                bgcolor: "#4f2ede",
                color: "white",
                padding: 1,
            }}
        >
            <h1>
                スプラ3-キルクリップメーカー
            </h1>
        </Box>
    );
}
