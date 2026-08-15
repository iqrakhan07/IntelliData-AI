from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


def generate_pdf_report(
    filename,
    df,
    experiments_df,
    insights,
    prediction=None,
    confidence=None,
    problem_type=None,
    target_column=None
):
    """
    Generate a professional IntelliData AI PDF report.
    """

    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # ==================================================
    # STYLES
    # ==================================================

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = styles["BodyText"]

    story = []

    # ==================================================
    # TITLE
    # ==================================================

    story.append(
        Paragraph(
            "IntelliData AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Intelligent Data Analytics & Machine Learning Report",
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ==================================================
    # DATASET SUMMARY
    # ==================================================

    story.append(
        Paragraph(
            "1. Dataset Summary",
            heading_style
        )
    )

    rows, columns = df.shape

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    summary_data = [
        ["Metric", "Value"],
        ["Rows", f"{rows:,}"],
        ["Columns", f"{columns:,}"],
        ["Missing Values", f"{missing_values:,}"],
        ["Duplicate Rows", f"{duplicate_rows:,}"]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            3 * inch,
            2 * inch
        ]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "CENTER"
            )
        ])
    )

    story.append(
        summary_table
    )

    story.append(
        Spacer(1, 20)
    )

    # ==================================================
    # DATASET COLUMNS
    # ==================================================

    story.append(
        Paragraph(
            "2. Dataset Columns",
            heading_style
        )
    )

    column_data = [
        [
            "Column",
            "Data Type",
            "Missing Values"
        ]
    ]

    for column in df.columns:

        column_data.append([
            str(column),
            str(df[column].dtype),
            str(
                df[column].isnull().sum()
            )
        ])

    column_table = Table(
        column_data,
        repeatRows=1,
        colWidths=[
            2.5 * inch,
            1.5 * inch,
            1.5 * inch
        ]
    )

    column_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            )
        ])
    )

    story.append(
        column_table
    )

    story.append(
        PageBreak()
    )

    # ==================================================
    # MACHINE LEARNING EXPERIMENTS
    # ==================================================

    story.append(
        Paragraph(
            "3. Machine Learning Experiments",
            heading_style
        )
    )

    if (
        experiments_df is not None
        and not experiments_df.empty
    ):

        experiment_data = [
            [
                "Algorithm",
                "Problem",
                "Target",
                "Score"
            ]
        ]

        for _, row in experiments_df.iterrows():

            try:
                score = float(
                    row["Score"]
                )

                score_text = f"{score:.4f}"

            except Exception:

                score_text = str(
                    row["Score"]
                )

            experiment_data.append([
                str(row["Algorithm"]),
                str(row["Problem Type"]),
                str(row["Target"]),
                score_text
            ])

        experiment_table = Table(
            experiment_data,
            repeatRows=1,
            colWidths=[
                1.6 * inch,
                1.3 * inch,
                1.5 * inch,
                1.0 * inch
            ]
        )

        experiment_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                )
            ])
        )

        story.append(
            experiment_table
        )

    else:

        story.append(
            Paragraph(
                "No machine learning experiments available.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 20)
    )

    # ==================================================
    # MODEL INFORMATION
    # ==================================================

    story.append(
        Paragraph(
            "4. Model Information",
            heading_style
        )
    )

    model_data = [
        ["Property", "Value"],
        [
            "Problem Type",
            str(
                problem_type
                if problem_type
                else "Not Available"
            )
        ],
        [
            "Target Column",
            str(
                target_column
                if target_column
                else "Not Available"
            )
        ]
    ]

    model_table = Table(
        model_data,
        colWidths=[
            2.5 * inch,
            3 * inch
        ]
    )

    model_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            )
        ])
    )

    story.append(
        model_table
    )

    story.append(
        Spacer(1, 20)
    )

    # ==================================================
    # LATEST PREDICTION
    # ==================================================

    story.append(
        Paragraph(
            "5. Latest Prediction",
            heading_style
        )
    )

    # ----------------------------------------------
    # Prediction label
    # ----------------------------------------------

    if prediction is None:

        prediction_text = (
            "No prediction generated"
        )

    else:

        if str(prediction) == "1":

            prediction_text = (
                "1 - Survived"
            )

        elif str(prediction) == "0":

            prediction_text = (
                "0 - Not Survived"
            )

        else:

            prediction_text = str(
                prediction
            )


    # ----------------------------------------------
    # Confidence
    # ----------------------------------------------

    if confidence is None:

        confidence_text = (
            "Not Available"
        )

    else:

        try:

            confidence_text = (
                f"{float(confidence):.2f}%"
            )

        except Exception:

            confidence_text = str(
                confidence
            )


    prediction_data = [
        ["Property", "Result"],

        [
            "Prediction",
            prediction_text
        ],

        [
            "Confidence",
            confidence_text
        ]
    ]


    prediction_table = Table(
        prediction_data,
        colWidths=[
            2.5 * inch,
            3 * inch
        ]
    )


    prediction_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "FONTNAME",
                (0, 1),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER"
            )
        ])
    )


    story.append(
        prediction_table
    )


    story.append(
        Spacer(1, 20)
    )

    # ==================================================
    # AI INSIGHTS
    # ==================================================

    story.append(
        Paragraph(
            "6. AI Insights",
            heading_style
        )
    )

    if insights:

        for insight in insights:

            story.append(
                Paragraph(
                    f"• {str(insight)}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 6)
            )

    else:

        story.append(
            Paragraph(
                "No AI insights available.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 20)
    )

    # ==================================================
    # CONCLUSION
    # ==================================================

    story.append(
        Paragraph(
            "7. Conclusion",
            heading_style
        )
    )

    if prediction is not None:

        conclusion = (
            "The IntelliData AI system successfully "
            "processed the uploaded dataset, evaluated "
            "machine learning experiments and generated "
            "a prediction using the selected model."
        )

    else:

        conclusion = (
            "The IntelliData AI system successfully "
            "analyzed the uploaded dataset and generated "
            "machine learning insights."
        )


    story.append(
        Paragraph(
            conclusion,
            normal_style
        )
    )

    story.append(
        Spacer(1, 30)
    )

    # ==================================================
    # FOOTER
    # ==================================================

    story.append(
        Paragraph(
            "Generated by IntelliData AI",
            normal_style
        )
    )

    # ==================================================
    # BUILD PDF
    # ==================================================

    document.build(
        story
    )