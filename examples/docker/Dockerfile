# Use any image as base image
FROM python:3.9-slim-bullseye

RUN python -m pip install amplpy --no-cache-dir
RUN python -m amplpy.modules install highs --no-cache-dir

# Add non-root user (optional)
ARG USERNAME=guest
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
# Change to non-root privilege
USER ${USERNAME}
