"""
Defines ImageButton class, a special Button that includes an image in a frame
and eventually some text next to it.
"""

import os
from typing import Callable, Sequence

import pygame

from .button import Button
from ..configuration import default_sprites
from ..constants import WHITE, MIDNIGHT_BLUE
from ..types import Position, Margin


class ImageButton(Button):
    """
    This component is a Button having an image displayed
    at the left of its content and that is considered as part of the button.
    The image is displayed in a dedicated square frame.

    Keyword arguments:
    callback -- the reference to the function that should be call after a click
    size -- the size of the button following the format "(width, height)"
    image_path -- the relative path to the image that should be displayed on the left
    title -- the text that should be displayed at the center of the element
    position -- the position of the element on the screen
    background_path -- the path to the image corresponding to the sprite of the element
    frame_background_path -- the path to the background for the frame
    frame_background_hover_path -- the path to the background for the frame when the mouse is over
    margin -- a tuple containing the margins of the box,
    should be in the form "(top_margin, right_margin, bottom_margin, left_margin)"
    linked_object -- the game entity linked to the button if there is one
    disabled -- a boolean indicating if it is not possible to interact with the button
    font -- the font that should be used to render the text content
    text_color -- the color of the text content
    font_hover -- the font that should be used to render the text content when the mouse is over
    the button
    text_hover_color -- the color of the text content when the mouse is over the button
    complementary_text_lines -- the other text lines that should be displayed in addition of
    the title
    """

    def __init__(
        self,
        callback: Callable,
        size: tuple[int, int],
        image_path: str,
        title: str = "",
        position: Position = pygame.Vector2(0, 0),
        background_path: str = None,
        frame_background_path: str = None,
        frame_background_hover_path: str = None,
        margin: Margin = (0, 0, 0, 0),
        linked_object: any = None,
        disabled: bool = False,
        font: pygame.font.Font = None,
        text_color: tuple[int, int, int] = WHITE,
        font_hover: pygame.font.Font = None,
        text_hover_color: tuple[int, int, int] = MIDNIGHT_BLUE,
        complementary_text_lines: Sequence[str] = None,
    ) -> None:
        super().__init__(
            callback,
            size,
            title,
            position,
            background_path,
            background_path,
            False,
            margin,
            linked_object,
            disabled,
            font,
            text_color,
            font_hover,
            text_hover_color,
            complementary_text_lines,
        )

        padding: int = size[1] // 10
        frame_position: Position = pygame.Vector2(padding, padding)
        frame_size: tuple[int, int] = (
            self.size[1] - padding * 2,
            self.size[1] - padding * 2,
        )
        image = pygame.transform.scale(
            pygame.image.load(image_path),
            (frame_size[0] - padding * 2, frame_size[1] - padding * 2),
        )

        frame_background_path = (
            os.path.abspath(frame_background_path)
            if frame_background_path
            else default_sprites["button_background"]["inactive"]
        )
        raw_frame = pygame.image.load(frame_background_path)
        frame = pygame.transform.scale(raw_frame.convert_alpha(), frame_size)
        frame.blit(image, (padding, padding))

        frame_background_hover_path = (
            os.path.abspath(frame_background_hover_path)
            if frame_background_hover_path
            else default_sprites["button_background"]["active"]
        )
        raw_frame_hover = pygame.image.load(frame_background_hover_path)
        frame_hover = pygame.transform.scale(
            raw_frame_hover.convert_alpha(), frame_size
        )
        frame_hover.blit(image, (padding, padding))

        self.sprite.blit(frame, frame_position)
        self.sprite_hover.blit(frame_hover, frame_position)

    def render_sprite(
        self, background_path: str, rendered_text_lines: Sequence[pygame.Surface]
    ) -> pygame.Surface:
        """
        Compute the rendering of the image button with the given background and text lines.
        Render the text lines next to the image frame.

        Return the generated pygame Surface.

        Keyword arguments:
        background_path -- the path to the image corresponding to the sprite of the button
        rendered_text_lines -- the sequence of text lines in order that should be clipped
        on the surface
        """
        raw_sprite = pygame.image.load(background_path)
        sprite = pygame.transform.scale(raw_sprite.convert_alpha(), self.size)

        text_lines_count = len(rendered_text_lines)

        for index, rendered_text_line in enumerate(rendered_text_lines):
            sprite.blit(
                rendered_text_line,
                (
                    self.size[1],
                    (2 * index + 1) * sprite.get_height() // (2 * text_lines_count)
                    - rendered_text_line.get_height() // 2,
                ),
            )
        return sprite
